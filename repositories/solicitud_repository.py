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
            cursor.execute('''
                SELECT s.*, 
                       a.nombre || ' ' || a.paterno || ' ' || a.materno as nombre_alumno,
                       m.nombre as municipio_nombre, 
                       c.descripcion as asunto_descripcion
                FROM solicitudes s
                JOIN alumnos a ON s.curp_alumno = a.curp
                JOIN municipios m ON s.municipio_id = m.id
                JOIN asuntos c ON s.asunto_id = c.id
            ''')
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

    def get_stats_by_municipio(self, municipio_id: Optional[int] = None, asunto_id: Optional[int] = None, nivel_id: Optional[int] = None) -> dict:
        try:
            cursor = self.db.cursor()
            stats = {'total': 0, 'pendientes': 0, 'resueltos': 0, 'por_municipio': [], 'por_asunto': [], 'por_nivel': []}
            
            # Base Joins
            base_join = '''
                FROM solicitudes s 
                JOIN alumnos a ON s.curp_alumno = a.curp
            '''
            
            # Dynamic WHERE clause
            conditions = []
            params = []
            
            if municipio_id:
                conditions.append("s.municipio_id = ?")
                params.append(municipio_id)
            if asunto_id:
                conditions.append("s.asunto_id = ?")
                params.append(asunto_id)
            if nivel_id:
                conditions.append("a.nivel_id = ?")
                params.append(nivel_id)
                
            where_clause = ""
            if conditions:
                where_clause = " WHERE " + " AND ".join(conditions)
                
            # KPI totals
            cursor.execute(f"SELECT COUNT(*), s.estatus {base_join} {where_clause} GROUP BY s.estatus", params)
            for count, estatus in cursor.fetchall():
                stats['total'] += count
                if estatus == 'Pendiente':
                    stats['pendientes'] = count
                elif estatus == 'Resuelto':
                    stats['resueltos'] = count
                    
            # By municipio
            cursor.execute(f'''
                SELECT m.id, m.nombre, COUNT(*) 
                {base_join} JOIN municipios m ON s.municipio_id = m.id 
                {where_clause} GROUP BY m.id
            ''', params)
            stats['por_municipio'] = [{'id': row[0], 'nombre': row[1], 'COUNT(*)': row[2]} for row in cursor.fetchall()]
            
            # By asunto
            cursor.execute(f'''
                SELECT asu.id, asu.descripcion, COUNT(*) 
                {base_join} JOIN asuntos asu ON s.asunto_id = asu.id 
                {where_clause} GROUP BY asu.id
            ''', params)
            stats['por_asunto'] = [{'id': row[0], 'descripcion': row[1], 'COUNT(*)': row[2]} for row in cursor.fetchall()]

            # By nivel educativo
            cursor.execute(f'''
                SELECT n.id, n.nombre, COUNT(*) 
                {base_join} JOIN niveles_educativos n ON a.nivel_id = n.id 
                {where_clause} GROUP BY n.id
            ''', params)
            stats['por_nivel'] = [{'id': row[0], 'nombre': row[1], 'COUNT(*)': row[2]} for row in cursor.fetchall()]
                
            return stats
        except Exception as e:
            print(f"[{datetime.now()}] Error get_stats_by_municipio: {e}")
            return {'total': 0, 'pendientes': 0, 'resueltos': 0, 'por_municipio': [], 'por_asunto': [], 'por_nivel': []}

    def cambiar_estatus(self, id: int, estatus: str) -> bool:
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE solicitudes SET estatus = ? WHERE id = ?", (estatus, id))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[{datetime.now()}] Error cambiar_estatus: {e}")
            return False
