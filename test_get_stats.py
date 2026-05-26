import os
import sys

sys.path.insert(0, os.path.abspath('.'))

import sqlite3
from repositories.solicitud_repository import SolicitudRepository
from database.connection import DatabaseConnection

class FakeDB:
    def __init__(self):
        self.conn = sqlite3.connect("ticket_turno.db")
        self.conn.row_factory = sqlite3.Row

# monkey patch
DatabaseConnection._instance = FakeDB()
DatabaseConnection._instance._initialized = True

repo = SolicitudRepository()
print("Calling get_stats_by_municipio...")
stats = repo.get_stats_by_municipio()
print(stats)
print("Done!")
