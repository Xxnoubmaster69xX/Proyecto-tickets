from database.connection import DatabaseConnection
from models.alumno import Alumno
from models.solicitud import Solicitud
from repositories.alumno_repository import AlumnoRepository
from repositories.solicitud_repository import SolicitudRepository
import random

def generar_datos_prueba():
    db = DatabaseConnection()
    db.initialize()
    
    alumno_repo = AlumnoRepository()
    solicitud_repo = SolicitudRepository()

    municipios = list(range(1, 39))  # 38 municipios de Coahuila
    niveles = [1, 2, 3, 4, 5]
    asuntos = [1, 2, 3, 4, 5, 6, 7]
    estatus_opts = ['Pendiente', 'Resuelto']

    nombres_alumnos = ["Ana", "Carlos", "Luis", "Maria", "Jose", "Pedro", "Juan", "Sofia"]
    apellidos = ["Perez", "Gomez", "Lopez", "Martinez", "Gonzalez", "Hernandez", "Ruiz", "Torres"]

    print("[DEMO] Generando 50 solicitudes de prueba...")
    
    for i in range(50):
        # Datos aleatorios
        nombre = random.choice(nombres_alumnos)
        paterno = random.choice(apellidos)
        materno = random.choice(apellidos)
        curp = f"{paterno[:2]}{materno[0]}{nombre[0]}080112HMC{paterno[1]}RV{i:02d}".upper()
        
        m_id = random.choice(municipios)
        n_id = random.choice(niveles)
        
        alumno = Alumno(curp, nombre, paterno, materno, n_id, m_id)
        alumno_repo.create_or_update(alumno)
        
        turno = solicitud_repo.get_next_turno_for_municipio(m_id)
        s = Solicitud(
            id=None,
            numero_turno=turno,
            curp_alumno=curp,
            quien_tramita=f"{paterno} {materno} Padre/Madre",
            telefono_principal=f"844{random.randint(1000000, 9999999)}",
            telefono_secundario="",
            correo=f"{nombre.lower()}{i}@example.com",
            asunto_id=random.choice(asuntos),
            municipio_id=m_id,
            estatus=random.choice(estatus_opts),
            observaciones="Solicitud generada auto para demo."
        )
        solicitud_repo.create(s)
        
    print("[DEMO] 50 solicitudes de prueba creadas exitosamente.")

if __name__ == "__main__":
    generar_datos_prueba()
