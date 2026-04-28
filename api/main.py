import os
import sys

# Ensure project root is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from database.connection import DatabaseConnection
from controllers.auth_controller import AuthController
from controllers.solicitud_controller import SolicitudController
from controllers.dashboard_controller import DashboardController
from controllers.admin_controller import AdminController
from utils.ticket_generator import generate_ticket_pdf

from api.schemas import LoginRequest, LoginResponse, SolicitudCreate, SolicitudUpdate, CatalogoItem

app = FastAPI(title="Ticket de Turno API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    DatabaseConnection().initialize()

# AUTH
@app.post("/api/auth/login", response_model=LoginResponse)
def login(req: LoginRequest):
    auth = AuthController()
    success, msg = auth.login(req.username, req.password)
    user = {"username": req.username} if success else None
    return LoginResponse(success=success, mensaje=msg, usuario=user)

# DASHBOARD
@app.get("/api/dashboard/stats")
def get_stats(municipio_id: int = None):
    dash = DashboardController()
    return dash.get_stats(municipio_id)

# SOLICITUDES
@app.post("/api/solicitudes")
def crear_solicitud(req: SolicitudCreate):
    controller = SolicitudController()
    success, msg, solicitud = controller.registrar_solicitud(req.dict())
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"success": True, "solicitud": solicitud.to_dict()}

@app.put("/api/solicitudes/{curp}/{turno}")
def modificar_solicitud(curp: str, turno: int, req: SolicitudUpdate):
    controller = SolicitudController()
    success, msg = controller.modificar_solicitud(curp, turno, req.dict(exclude_unset=True))
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"success": True}

@app.get("/api/solicitudes/buscar")
def buscar_solicitudes(curp: str = None, nombre: str = None):
    controller = SolicitudController()
    if curp:
        res = controller.buscar_por_curp(curp)
    elif nombre:
        res = controller.buscar_por_nombre(nombre)
    else:
        res = controller.repo.get_all()
    return [s.to_dict() for s in res]

@app.put("/api/solicitudes/{id}/estatus")
def cambiar_estatus(id: int, estatus: str):
    controller = SolicitudController()
    success, msg = controller.cambiar_estatus(id, estatus)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"success": True}

@app.delete("/api/solicitudes/{id}")
def eliminar_solicitud(id: int):
    controller = SolicitudController()
    success, msg = controller.eliminar_solicitud(id)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"success": True}

@app.get("/api/solicitudes/{id}/pdf")
def descargar_pdf(id: int):
    controller = SolicitudController()
    solicitud = controller.repo.get_by_id(id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="No encontrada")
    
    pdf_bytes = generate_ticket_pdf(solicitud)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=Turno_{solicitud.numero_turno}.pdf"})

# CATALOGOS
@app.get("/api/catalogos/{tipo}")
def get_catalogo(tipo: str):
    admin = AdminController()
    if tipo == 'municipio': return [m.to_dict() for m in admin.get_municipios()]
    if tipo == 'nivel': return [n.to_dict() for n in admin.get_niveles()]
    if tipo == 'asunto': return [a.to_dict() for a in admin.get_asuntos()]
    raise HTTPException(status_code=400, detail="Catálogo inválido")

@app.post("/api/catalogos/{tipo}")
def crear_catalogo(tipo: str, item: CatalogoItem):
    admin = AdminController()
    val = item.nombre or item.descripcion
    if not val:
        raise HTTPException(status_code=400, detail="Valor requerido")
    if not admin.create_catalogo(tipo, val):
        raise HTTPException(status_code=400, detail="Error al crear")
    return {"success": True}

@app.put("/api/catalogos/{tipo}/{id}")
def update_catalogo(tipo: str, id: int, item: CatalogoItem):
    admin = AdminController()
    val = item.nombre or item.descripcion
    if not admin.update_catalogo(tipo, id, val):
        raise HTTPException(status_code=400, detail="Error al actualizar")
    return {"success": True}

@app.delete("/api/catalogos/{tipo}/{id}")
def delete_catalogo(tipo: str, id: int):
    admin = AdminController()
    if not admin.delete_catalogo(tipo, id):
        raise HTTPException(status_code=400, detail="No se pudo borrar porque está en uso")
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
