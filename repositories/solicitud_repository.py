from typing import Optional, List
from .base_repository import BaseRepository
from models.solicitud import Solicitud
from database.connection import DatabaseConnection
from datetime import datetime

class SolicitudRepository(BaseRepository[Solicitud]):
    def __init__(self):
        self.db = DatabaseConnection().conn

    def _map_row_to_entity(self, row) -> Solicitud:
        s = Solicitud(
            id=row['id'],
            numero_turno=row['numero_turno'],
            curp_alumno=row['curp_alumno'],
            quien_tramita=row['quien_tramita'],
            telefono_principal=row['telefono_principal'],
            telefono_secundario=row['telefono_secundario'],
            correo=row['correo'],
            asunto_id=row['asunto_id'],
            municipio_id=row['municipio_id'],
            estatus=row['estatus'],
            observaciones=row['observaciones'],
            creado_en=row['creado_en'],
            actualizado_en=row['actualizado_en']
        )
        if 'nombre_alumno' in row.keys():
            s.nombre_alumno = row['nombre_alumno']
        if 'municipio_nombre' in row.keys():
            s.municipio_nombre = row['municipio_nombre']
        if 'asunto_descripcion' in row.keys():
            s.asunto_descripcion = row['asunto_descripcion']
        return s

    def get_by_id(self, id: int) -> Optional[Solicitud]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM solicitudes WHERE id = ?", (id,))
            row = cursor.fetchone()
            return self._map_row_to_entity(row) if row else None
        except Exception as e:
            print(f"[{datetime.now()}] Error get_by_id: {e}")
            return None

    def get_all(self) -> List[Solicitud]:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM solicitudes")
            return [self._map_row_to_entity(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"[{datetime.now()}] Error get_all: {e}")
            return []

    def create(self, s: Solicitud) -> Solicitud:
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT INTO solicitudes (numero_turno, curp_alumno, quien_tramita, telefono_principal,
                                         telefono_secundario, correo, asunto_id, municipio_id, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (s.numero_turno, s.curp_alumno, s.quien_tramita, s.telefono_principal,
                  s.telefono_secundario, s.correo, s.asunto_id, s.municipio_id, s.observaciones))
            self.db.commit()
            s.id = cursor.lastrowid
            return s
        except Exception as e:
            print(f"[{datetime.now()}] Error create: {e}")
            raise Exception(f"No se pudo crear la solicitud. {str(e)}")

    def update(self, s: Solicitud) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                UPDATE solicitudes
                SET quien_tramita=?, telefono_principal=?, telefono_secundario=?, correo=?,
                    asunto_id=?, municipio_id=?, observaciones=?
                WHERE id=?
            ''', (s.quien_tramita, s.telefono_principal, s.telefono_secundario, s.correo,
                  s.asunto_id, s.municipio_id, s.observaciones, s.id))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error update: {e}")
            return False

    def delete(self, id: int) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM solicitudes WHERE id = ?", (id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error delete: {e}")
            return False

    def get_by_curp(self, curp: str) -> List[Solicitud]:
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT s.*, a.nombre || ' ' || a.paterno || ' ' || a.materno as nombre_alumno,
                       m.nombre as municipio_nombre, c.descripcion as asunto_descripcion
                FROM solicitudes s
                JOIN alumnos a ON s.curp_alumno = a.curp
                JOIN municipios m ON s.municipio_id = m.id
                JOIN asuntos c ON s.asunto_id = c.id
                WHERE s.curp_alumno = ?
            ''', (curp,))
            return [self._map_row_to_entity(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"[{datetime.now()}] Error get_by_curp: {e}")
            return []

    def get_by_nombre_alumno(self, nombre: str) -> List[Solicitud]:
        try:
            cursor = self.db.cursor()
            search = f"%{nombre}%"
            cursor.execute('''
                SELECT s.*, 
                       a.nombre || ' ' || a.paterno || ' ' || a.materno as nombre_alumno,
                       m.nombre as municipio_nombre, 
                       c.descripcion as asunto_descripcion
                FROM solicitudes s
                JOIN alumnos a ON s.curp_alumno = a.curp
                JOIN municipios m ON s.municipio_id = m.id
                JOIN asuntos c ON s.asunto_id = c.id
                WHERE a.nombre LIKE ? OR a.paterno LIKE ? OR a.materno LIKE ?
            ''', (search, search, search))
            return [self._map_row_to_entity(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"[{datetime.now()}] Error get_by_nombre_alumno: {e}")
            return []

    def get_by_turno_and_curp(self, numero_turno: int, curp: str) -> Optional[Solicitud]:
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT s.*, a.nombre || ' ' || a.paterno || ' ' || a.materno as nombre_alumno,
                       m.nombre as municipio_nombre, c.descripcion as asunto_descripcion
                FROM solicitudes s
                JOIN alumnos a ON s.curp_alumno = a.curp
                JOIN municipios m ON s.municipio_id = m.id
                JOIN asuntos c ON s.asunto_id = c.id
                WHERE s.numero_turno = ? AND s.curp_alumno = ?
            ''', (numero_turno, curp))
            row = cursor.fetchone()
            return self._map_row_to_entity(row) if row else None
        except Exception as e:
            print(f"[{datetime.now()}] Error get_by_turno_and_curp: {e}")
            return None

    def get_next_turno_for_municipio(self, municipio_id: int) -> int:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT MAX(numero_turno) FROM solicitudes WHERE municipio_id = ?", (municipio_id,))
            max_turno = cursor.fetchone()[0]
            return (max_turno or 0) + 1
        except Exception as e:
            print(f"[{datetime.now()}] Error get_next_turno_for_municipio: {e}")
            return 1

    def get_stats_by_municipio(self, municipio_id: Optional[int]) -> dict:
        try:
            cursor = self.db.cursor()
            stats = {'total': 0, 'pendientes': 0, 'resueltos': 0, 'por_municipio': [], 'por_asunto': []}
            
            # KPI totals
            if municipio_id:
                cursor.execute("SELECT COUNT(*), estatus FROM solicitudes WHERE municipio_id = ? GROUP BY estatus", (municipio_id,))
            else:
                cursor.execute("SELECT COUNT(*), estatus FROM solicitudes GROUP BY estatus")
                
            for count, estatus in cursor.fetchall():
                stats['total'] += count
                if estatus == 'Pendiente':
                    stats['pendientes'] = count
                elif estatus == 'Resuelto':
                    stats['resueltos'] = count
                    
            # By municipio
            if not municipio_id:
                cursor.execute('''
                    SELECT m.nombre, COUNT(*) 
                    FROM solicitudes s JOIN municipios m ON s.municipio_id = m.id 
                    GROUP BY m.id
                ''')
                stats['por_municipio'] = cursor.fetchall()
            
            # By asunto
            if municipio_id:
                cursor.execute('''
                    SELECT a.descripcion, COUNT(*) 
                    FROM solicitudes s JOIN asuntos a ON s.asunto_id = a.id 
                    WHERE s.municipio_id = ? GROUP BY a.id
                ''', (municipio_id,))
            else:
                cursor.execute('''
                    SELECT a.descripcion, COUNT(*) 
                    FROM solicitudes s JOIN asuntos a ON s.asunto_id = a.id 
                    GROUP BY a.id
                ''')
            stats['por_asunto'] = cursor.fetchall()
                
            return stats
        except Exception as e:
            print(f"[{datetime.now()}] Error get_stats_by_municipio: {e}")
            return {'total': 0, 'pendientes': 0, 'resueltos': 0, 'por_municipio': [], 'por_asunto': []}

    def cambiar_estatus(self, id: int, estatus: str) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE solicitudes SET estatus = ? WHERE id = ?", (estatus, id))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error cambiar_estatus: {e}")
            return False
