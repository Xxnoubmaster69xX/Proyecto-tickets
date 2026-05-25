# Modificado por Miguel para el commit
import urllib.request
import json
import time

# Get tickets
req = urllib.request.Request("http://localhost:8000/api/solicitudes/buscar")
res = urllib.request.urlopen(req)
data = json.loads(res.read())

count = 0
for ticket in data:
    if count >= 36:
        break
    if ticket['estatus'] == 'Pendiente':
        url = f"http://localhost:8000/api/solicitudes/{ticket['id']}/estatus?estatus=Resuelto"
        req_put = urllib.request.Request(url, method='PUT')
        urllib.request.urlopen(req_put)
        count += 1
        time.sleep(0.01)

print(f"¡{count} tickets actualizados a Resuelto vía API!")
