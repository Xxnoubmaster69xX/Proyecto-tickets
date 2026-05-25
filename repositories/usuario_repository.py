from typing import Optional, List
from .base_repository import BaseRepository
from models.usuario import Usuario
from database.connection import DatabaseConnection
import bcrypt
from datetime import datetime

class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self):
        self.db = DatabaseConnection().conn

    def _map_row_to_entity(self, row) -> Usuario:
        return Usuario(
            id=row['id'],
            username=row['username'],
            password_hash=row['password_hash'],
            nombre_completo=row['nombre_completo'],
            activo=row['activo'],
            creado_en=row['creado_en']
        )

    def get_by_id(self, id: int) -> Optional[Usuario]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
            row = cursor.fetchone()
            return self._map_row_to_entity(row) if row else None
        except Exception as e:
            print(f"[{datetime.now()}] Error get_by_id: {e}")
            return None

    def get_all(self) -> List[Usuario]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM usuarios")
            rows = cursor.fetchall()
            return [self._map_row_to_entity(row) for row in rows]
        except Exception as e:
            print(f"[{datetime.now()}] Error get_all usuario: {e}")
            return []

    def create(self, entity: Usuario) -> Usuario:
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT INTO usuarios (username, password_hash, nombre_completo, activo, creado_en)
                VALUES (?, ?, ?, ?, ?)
            ''', (entity.username, entity.password_hash, entity.nombre_completo, entity.activo, entity.creado_en))
            self.db.commit()
            entity.id = cursor.lastrowid
            return entity
        except Exception as e:
            print(f"[{datetime.now()}] Error create usuario: {e}")
            raise

    def update(self, entity: Usuario) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                UPDATE usuarios SET username=?, password_hash=?, nombre_completo=?, activo=?
                WHERE id=?
            ''', (entity.username, entity.password_hash, entity.nombre_completo, entity.activo, entity.id))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error update usuario: {e}")
            return False

    def delete(self, id: int) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error delete usuario: {e}")
            return False

    def get_by_username(self, username: str) -> Optional[Usuario]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username = ? AND activo = 1", (username,))
            row = cursor.fetchone()
            return self._map_row_to_entity(row) if row else None
        except Exception as e:
            print(f"[{datetime.now()}] Error get_by_username: {e}")
            return None

    def verify_password(self, username: str, password: str) -> Optional[Usuario]:
        usuario = self.get_by_username(username)
        if usuario:
            try:
                if bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
                    return usuario
            except Exception as e:
                print(f"[{datetime.now()}] Error bcrypt: {e}")
        return None
