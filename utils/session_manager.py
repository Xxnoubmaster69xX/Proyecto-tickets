from typing import Optional
from models.usuario import Usuario

class SessionManager:
    """
    Maneja la sesión activa del administrador.
    Singleton que almacena el usuario autenticado.
    Al logout destruye todas las referencias de sesión.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._current_user: Optional[Usuario] = None
        return cls._instance

    def login(self, usuario: Usuario) -> None:
        self._current_user = usuario

    def logout(self) -> None:
        self._current_user = None

    @property
    def is_authenticated(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> Optional[Usuario]:
        return self._current_user
