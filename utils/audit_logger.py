from patterns.event_bus import EventBus, AppEvent
from repositories.bitacora_repository import BitacoraRepository
from models.bitacora import Bitacora
from utils.session_manager import SessionManager

class AuditLogger:
    """
    Servicio de auditoría del sistema que escucha los eventos globales
    de la aplicación y registra automáticamente las acciones en la base de datos.
    Desacoplado usando el patrón Observer (EventBus).
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.repo = BitacoraRepository()
            cls._instance._initialized = False
        return cls._instance

    def initialize(self):
        if not self._initialized:
            bus = EventBus()
            bus.subscribe(AppEvent.SOLICITUD_CREADA, self.on_solicitud_creada)
            bus.subscribe(AppEvent.SOLICITUD_ACTUALIZADA, self.on_solicitud_actualizada)
            bus.subscribe(AppEvent.SOLICITUD_ELIMINADA, self.on_solicitud_eliminada)
            bus.subscribe(AppEvent.ESTATUS_CAMBIADO, self.on_estatus_cambiado)
            bus.subscribe(AppEvent.LOGIN_EXITOSO, self.on_login)
            bus.subscribe(AppEvent.LOGOUT, self.on_logout)
            bus.subscribe(AppEvent.CATALOGO_ACTUALIZADO, self.on_catalogo_actualizado)
            self._initialized = True

    def _get_current_username(self) -> str:
        user = SessionManager().current_user
        return user.username if user else "Público"

    def on_solicitud_creada(self, solicitud):
        self.repo.create(Bitacora(
            id=None,
            usuario=self._get_current_username(),
            accion="REGISTRO_TICKET",
            detalle=f"Se creó el ticket #{solicitud.numero_turno} para CURP: {solicitud.curp_alumno}."
        ))

    def on_solicitud_actualizada(self, solicitud):
        self.repo.create(Bitacora(
            id=None,
            usuario=self._get_current_username(),
            accion="MODIFICACION_TICKET",
            detalle=f"Se modificaron los datos del ticket #{solicitud.numero_turno} (CURP: {solicitud.curp_alumno})."
        ))

    def on_solicitud_eliminada(self, id_solicitud):
        self.repo.create(Bitacora(
            id=None,
            usuario=self._get_current_username(),
            accion="ELIMINACION_TICKET",
            detalle=f"Se eliminó permanentemente el ticket ID: {id_solicitud}."
        ))

    def on_estatus_cambiado(self, data):
        self.repo.create(Bitacora(
            id=None,
            usuario=self._get_current_username(),
            accion="CAMBIO_ESTATUS",
            detalle=f"Se cambió el estatus del ticket ID: {data.get('id')} a '{data.get('nuevo_estatus')}'."
        ))

    def on_login(self, user):
        self.repo.create(Bitacora(
            id=None,
            usuario=user.username,
            accion="INICIO_SESION",
            detalle=f"El administrador {user.nombre_completo} inició sesión."
        ))

    def on_logout(self, data):
        self.repo.create(Bitacora(
            id=None,
            usuario="admin",  # En logout el usuario ya se borró de la sesión, se infiere
            accion="CERRAR_SESION",
            detalle="El administrador cerró la sesión de forma segura."
        ))

    def on_catalogo_actualizado(self, tipo):
        self.repo.create(Bitacora(
            id=None,
            usuario=self._get_current_username(),
            accion="CATALOGO_MODIFICADO",
            detalle=f"Se realizó una modificación en el catálogo: {tipo}."
        ))
