from typing import Optional, List
from .base_repository import BaseRepository
from models.alumno import Alumno
from database.connection import DatabaseConnection
from datetime import datetime

class AlumnoRepository(BaseRepository[Alumno]):
    def __init__(self):
        self.db = DatabaseConnection().conn

    def get_by_id(self, id: str) -> Optional[Alumno]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM alumnos WHERE curp = ?", (id,))
            row = cursor.fetchone()
            return Alumno(**row) if row else None
        except Exception as e:
            print(f"[{datetime.now()}] Error get_by_id alumno: {e}")
            return None

    def get_all(self) -> List[Alumno]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM alumnos")
            rows = cursor.fetchall()
            return [Alumno(**row) for row in rows]
        except Exception as e:
            print(f"[{datetime.now()}] Error get_all alumno: {e}")
            return []

    def create(self, a: Alumno) -> Alumno:
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT INTO alumnos (curp, nombre, paterno, materno, nivel_id, municipio_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (a.curp, a.nombre, a.paterno, a.materno, a.nivel_id, a.municipio_id))
            self.db.commit()
            return a
        except Exception as e:
            print(f"[{datetime.now()}] Error create alumno: {e}")
            raise

    def update(self, a: Alumno) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                UPDATE alumnos SET nombre=?, paterno=?, materno=?, nivel_id=?, municipio_id=?
                WHERE curp=?
            ''', (a.nombre, a.paterno, a.materno, a.nivel_id, a.municipio_id, a.curp))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error update alumno: {e}")
            return False

    def delete(self, id: str) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM alumnos WHERE curp = ?", (id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error delete alumno: {e}")
            return False

    def create_or_update(self, a: Alumno) -> Alumno:
        existing = self.get_by_id(a.curp)
        if existing:
            self.update(a)
        else:
            self.create(a)
        return a
