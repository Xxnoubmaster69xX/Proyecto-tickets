from typing import List, Optional
from database.connection import DatabaseConnection
from models.municipio import Municipio
from models.nivel_educativo import NivelEducativo
from models.asunto import Asunto
from datetime import datetime

class CatalogoRepository:
    def __init__(self):
        self.db = DatabaseConnection().conn

    # Municipios
    def get_municipios(self) -> List[Municipio]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM municipios WHERE activo = 1 ORDER BY nombre")
            return [Municipio(**row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"[{datetime.now()}] Error get_municipios: {e}")
            return []

    def create_municipio(self, nombre: str) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO municipios (nombre) VALUES (?)", (nombre,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[{datetime.now()}] Error create_municipio: {e}")
            return False

    def update_municipio(self, id: int, nombre: str) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE municipios SET nombre = ? WHERE id = ?", (nombre, id))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error update_municipio: {e}")
            return False

    def delete_municipio(self, id: int) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE municipios SET activo = 0 WHERE id = ?", (id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error delete_municipio: {e}")
            return False

    # Niveles Educativos
    def get_niveles(self) -> List[NivelEducativo]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM niveles_educativos WHERE activo = 1 ORDER BY id")
            return [NivelEducativo(**row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"[{datetime.now()}] Error get_niveles: {e}")
            return []

    def create_nivel(self, nombre: str) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO niveles_educativos (nombre) VALUES (?)", (nombre,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[{datetime.now()}] Error create_nivel: {e}")
            return False

    def update_nivel(self, id: int, nombre: str) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE niveles_educativos SET nombre = ? WHERE id = ?", (nombre, id))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[{datetime.now()}] Error update_nivel: {e}")
            return False

    def delete_nivel(self, id: int) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE niveles_educativos SET activo = 0 WHERE id = ?", (id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error delete_nivel: {e}")
            return False

    # Asuntos
    def get_asuntos(self) -> List[Asunto]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM asuntos WHERE activo = 1 ORDER BY id")
            return [Asunto(**row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"[{datetime.now()}] Error get_asuntos: {e}")
            return []

    def create_asunto(self, descripcion: str) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO asuntos (descripcion) VALUES (?)", (descripcion,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[{datetime.now()}] Error create_asunto: {e}")
            return False

    def update_asunto(self, id: int, descripcion: str) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE asuntos SET descripcion = ? WHERE id = ?", (descripcion, id))
            self.db.commit()
            return True
        except Exception as e:
            print(f"[{datetime.now()}] Error update_asunto: {e}")
            return False

    def delete_asunto(self, id: int) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE asuntos SET activo = 0 WHERE id = ?", (id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error delete_asunto: {e}")
            return False
