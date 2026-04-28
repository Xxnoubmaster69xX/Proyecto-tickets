import sqlite3
import threading
from pathlib import Path

class DatabaseConnection:
    """
    Singleton thread-safe para la conexión SQLite.
    Garantiza una única instancia durante el ciclo de vida de la app.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def initialize(self, db_path: str = "ticket_turno.db"):
        if not self._initialized:
            self._db_path = db_path
            self._connection = sqlite3.connect(db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row  # acceso por nombre de columna
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._run_migrations()
            self._initialized = True

    def _run_migrations(self):
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, "r", encoding="utf-8") as f:
            self._connection.executescript(f.read())
        self._connection.commit()

    @property
    def conn(self) -> sqlite3.Connection:
        return self._connection

    def close(self):
        """Cerrar limpiamente la BD al salir de la app."""
        if self._initialized and self._connection:
            self._connection.close()
            self._initialized = False
            DatabaseConnection._instance = None
