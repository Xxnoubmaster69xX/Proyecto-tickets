from typing import List, Optional
from .base_repository import BaseRepository
from models.bitacora import Bitacora
from database.connection import DatabaseConnection
from datetime import datetime

class BitacoraRepository(BaseRepository[Bitacora]):
    def __init__(self):
        self.db = DatabaseConnection().conn

    def get_by_id(self, id: int) -> Optional[Bitacora]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM bitacora WHERE id = ?", (id,))
            row = cursor.fetchone()
            return Bitacora(**row) if row else None
        except Exception as e:
            print(f"[{datetime.now()}] Error get_by_id bitacora: {e}")
            return None

    def get_all(self) -> List[Bitacora]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM bitacora ORDER BY creado_en DESC LIMIT 300")
            return [Bitacora(**row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"[{datetime.now()}] Error get_all bitacora: {e}")
            return []

    def create(self, b: Bitacora) -> Bitacora:
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT INTO bitacora (usuario, accion, detalle)
                VALUES (?, ?, ?)
            ''', (b.usuario, b.accion, b.detalle))
            self.db.commit()
            b.id = cursor.lastrowid
            return b
        except Exception as e:
            print(f"[{datetime.now()}] Error create bitacora: {e}")
            return b

    def update(self, b: Bitacora) -> bool:
        return False

    def delete(self, id: int) -> bool:
        return False
