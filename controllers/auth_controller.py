from typing import Tuple
from repositories.usuario_repository import UsuarioRepository
from utils.session_manager import SessionManager
from patterns.event_bus import EventBus, AppEvent
from database.connection import DatabaseConnection

class AuthController:
    def __init__(self):
        self.repo = UsuarioRepository()

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        usuario = self.repo.verify_password(username, password)
        if usuario:
            SessionManager().login(usuario)
            EventBus().publish(AppEvent.LOGIN_EXITOSO, usuario)
            return True, ""
        return False, "Credenciales incorrectas o usuario inactivo."

    def logout(self) -> None:
        SessionManager().logout()
        EventBus().publish(AppEvent.LOGOUT)
