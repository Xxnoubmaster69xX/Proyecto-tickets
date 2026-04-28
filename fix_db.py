import sqlite3

conn = sqlite3.connect('ticket_turno.db', timeout=10)
cursor = conn.cursor()
cursor.execute("UPDATE solicitudes SET estatus = 'Resuelto' WHERE id IN (SELECT id FROM solicitudes LIMIT 36);")
conn.commit()
conn.close()
print("36 tickets resueltos!")
