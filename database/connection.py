import sqlite3
import threading
from pathlib import Path

class DatabaseConnection:
    """
    Singleton thread-safe para la conexión SQLite.
    Garantiza una instancia por hilo usando threading.local()
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
                    cls._instance._local = threading.local()
        return cls._instance

    def initialize(self, db_path: str = "ticket_turno.db"):
        if not self._initialized:
            self._db_path = db_path
            # Run migrations on the main thread
            conn = sqlite3.connect(db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            
            schema_path = Path(__file__).parent / "schema.sql"
            with open(schema_path, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()
            conn.close()
            
            self._initialized = True

    @property
    def conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self._db_path, check_same_thread=False)
            self._local.connection.row_factory = sqlite3.Row
            self._local.connection.execute("PRAGMA foreign_keys = ON")
        return self._local.connection

    def close(self):
        """Cerrar limpiamente la BD al salir de la app."""
        if hasattr(self, '_local') and hasattr(self._local, 'connection'):
            self._local.connection.close()
            del self._local.connection

