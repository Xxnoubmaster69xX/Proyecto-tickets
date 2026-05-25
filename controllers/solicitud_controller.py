from typing import Tuple, Optional, List
from models.solicitud import Solicitud
from models.alumno import Alumno
from repositories.solicitud_repository import SolicitudRepository
from repositories.alumno_repository import AlumnoRepository
from utils.curp_validator import validate_curp
from patterns.event_bus import EventBus, AppEvent

class SolicitudController:
    def __init__(self):
        self.repo = SolicitudRepository()
        self.alumno_repo = AlumnoRepository()

    def registrar_solicitud(self, datos: dict) -> Tuple[bool, str, Optional[Solicitud]]:
        is_valid, curp_err = validate_curp(datos.get('curp_alumno', ''))
        if not is_valid:
            return False, curp_err, None

        campos_obligatorios = ['nombre', 'paterno', 'materno', 'nivel_id', 'municipio_id', 
                               'curp_alumno', 'quien_tramita', 'telefono_principal', 'correo', 'asunto_id']
        for c in campos_obligatorios:
            val = datos.get(c)
            if val is None or str(val).strip() == "":
                return False, f"El campo {c} es obligatorio.", None

        try:
            alumno = Alumno(
                curp=datos['curp_alumno'].upper(),
                nombre=datos['nombre'],
                paterno=datos['paterno'],
                materno=datos['materno'],
                nivel_id=int(datos['nivel_id']),
                municipio_id=int(datos['municipio_id'])
            )
            self.alumno_repo.create_or_update(alumno)

            numero_turno = self.repo.get_next_turno_for_municipio(int(datos['municipio_id']))

            solicitud = Solicitud(
                id=None,
                numero_turno=numero_turno,
                curp_alumno=alumno.curp,
                quien_tramita=datos['quien_tramita'],
                telefono_principal=datos['telefono_principal'],
                telefono_secundario=datos.get('telefono_secundario', None),
                correo=datos['correo'],
                asunto_id=int(datos['asunto_id']),
                municipio_id=int(datos['municipio_id']),
                estatus='Pendiente',
                observaciones=datos.get('observaciones', None)
            )

            solicitud_creada = self.repo.create(solicitud)
            EventBus().publish(AppEvent.SOLICITUD_CREADA, solicitud_creada)
            return True, "", self.repo.get_by_id(solicitud_creada.id)
        except Exception as e:
            return False, f"Error al registrar: {e}", None

    def modificar_solicitud(self, curp: str, numero_turno: int, datos: dict) -> Tuple[bool, str]:
        solicitud = self.repo.get_by_turno_and_curp(numero_turno, curp.upper())
        if not solicitud:
            return False, "No se encontró la solicitud con el turno y CURP especificados."

        try:
            solicitud.quien_tramita = datos.get('quien_tramita', solicitud.quien_tramita)
            solicitud.telefono_principal = datos.get('telefono_principal', solicitud.telefono_principal)
            solicitud.telefono_secundario = datos.get('telefono_secundario', solicitud.telefono_secundario)
            solicitud.correo = datos.get('correo', solicitud.correo)
            solicitud.observaciones = datos.get('observaciones', solicitud.observaciones)
            if 'asunto_id' in datos:
                solicitud.asunto_id = int(datos['asunto_id'])

            if 'estatus' in datos:
                solicitud.estatus = datos['estatus']

            ok = self.repo.update(solicitud)
            if ok:
                EventBus().publish(AppEvent.SOLICITUD_ACTUALIZADA, solicitud)
                if 'estatus' in datos:
                    EventBus().publish(AppEvent.ESTATUS_CAMBIADO, {'id': solicitud.id, 'nuevo_estatus': solicitud.estatus})
                return True, ""
            return False, "No se pudo actualizar."
        except Exception as e:
            return False, f"Error: {e}"

    def buscar_por_curp(self, curp: str) -> List[Solicitud]:
        return self.repo.get_by_curp(curp.upper())

    def buscar_por_nombre(self, nombre: str) -> List[Solicitud]:
        if not nombre.strip():
            return []
        return self.repo.get_by_nombre_alumno(nombre)

    def buscar_por_turno_y_curp(self, turno: int, curp: str) -> Optional[Solicitud]:
        return self.repo.get_by_turno_and_curp(turno, curp.upper())

    def cambiar_estatus(self, id: int, estatus: str) -> Tuple[bool, str]:
        if estatus not in ('Pendiente', 'Resuelto'):
            return False, "Estatus inválido."
        ok = self.repo.cambiar_estatus(id, estatus)
        if ok:
            EventBus().publish(AppEvent.ESTATUS_CAMBIADO, {'id': id, 'nuevo_estatus': estatus})
            return True, ""
        return False, "Error al cambiar estatus."

    def eliminar_solicitud(self, id: int) -> Tuple[bool, str]:
        ok = self.repo.delete(id)
        if ok:
            EventBus().publish(AppEvent.SOLICITUD_ELIMINADA, id)
            return True, ""
        return False, "Error al eliminar."
