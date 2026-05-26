import urllib.request
import json
import random
import time

municipios = list(range(1, 39))
niveles = [1, 2, 3, 4, 5]
asuntos = [1, 2, 3, 4, 5, 6, 7]

nombres = ["Ana", "Carlos", "Luis", "Maria", "Jose", "Pedro", "Juan", "Sofia"]
apellidos = ["Perez", "Gomez", "Lopez", "Martinez", "Gonzalez", "Hernandez", "Ruiz", "Torres"]

for i in range(50):
    nombre = random.choice(nombres)
    paterno = random.choice(apellidos)
    materno = random.choice(apellidos)
    curp = f"{paterno[:2]}{materno[0]}{nombre[0]}080112HMC{paterno[1]}RV{i:02d}".upper()

    payload = {
        "curp_alumno": curp,
        "nombre": nombre,
        "paterno": paterno,
        "materno": materno,
        "nivel_id": random.choice(niveles),
        "municipio_id": random.choice(municipios),
        "asunto_id": random.choice(asuntos),
        "quien_tramita": f"{paterno} Padre",
        "telefono_principal": f"844{random.randint(1000000, 9999999)}",
        "telefono_secundario": "",
        "correo": f"{nombre.lower()}{i}@example.com",
        "observaciones": "Solicitud generada auto via API."
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request("http://localhost:8000/api/solicitudes", data=data, headers={'Content-Type': 'application/json'})
    
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print("Error:", e)
        
    time.sleep(0.05)

print("¡50 registros inyectados vía API correctamente!")
