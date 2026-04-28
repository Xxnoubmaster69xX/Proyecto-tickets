from typing import Callable, Dict, List, Any
from enum import Enum

class AppEvent(Enum):
    """Eventos tipados de la aplicación."""
    SOLICITUD_CREADA      = "solicitud_creada"
    SOLICITUD_ACTUALIZADA = "solicitud_actualizada"
    SOLICITUD_ELIMINADA   = "solicitud_eliminada"
    ESTATUS_CAMBIADO      = "estatus_cambiado"
    LOGIN_EXITOSO         = "login_exitoso"
    LOGOUT                = "logout"
    CATALOGO_ACTUALIZADO  = "catalogo_actualizado"
    DASHBOARD_REFRESH     = "dashboard_refresh"

class EventBus:
    """
    Singleton que implementa el patrón Observer/Publisher-Subscriber.
    Desacopla publishers y subscribers usando eventos tipados.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribers: Dict[AppEvent, List[Callable]] = {}
        return cls._instance

    def subscribe(self, event: AppEvent, callback: Callable) -> None:
        if event not in self._subscribers:
            self._subscribers[event] = []
        self._subscribers[event].append(callback)

    def unsubscribe(self, event: AppEvent, callback: Callable) -> None:
        if event in self._subscribers:
            self._subscribers[event] = [
                cb for cb in self._subscribers[event] if cb != callback
            ]

    def publish(self, event: AppEvent, data: Any = None) -> None:
        for callback in self._subscribers.get(event, []):
            try:
                callback(data)
            except Exception as e:
                print(f"[EventBus] Error en callback para {event}: {e}")

    def clear_all(self) -> None:
        """Llamado al logout para limpiar suscripciones activas."""
        self._subscribers.clear()
