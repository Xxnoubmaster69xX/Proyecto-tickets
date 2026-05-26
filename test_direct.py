import sqlite3
import time

print("Connecting to DB...")
db = sqlite3.connect("ticket_turno.db", timeout=10.0)
c = db.cursor()

print("Running query...")
start = time.time()
try:
    c.execute("SELECT COUNT(*) FROM solicitudes s JOIN alumnos a ON s.curp_alumno = a.curp")
    print(c.fetchall())
except Exception as e:
    print("Error:", e)
print(f"Time taken: {time.time() - start:.2f}s")
