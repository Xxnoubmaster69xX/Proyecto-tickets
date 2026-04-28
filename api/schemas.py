from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    mensaje: str
    usuario: Optional[dict] = None

class SolicitudCreate(BaseModel):
    curp_alumno: str
    nombre: str
    paterno: str
    materno: str
    nivel_id: int
    municipio_id: int
    asunto_id: int
    quien_tramita: str
    telefono_principal: str
    telefono_secundario: Optional[str] = None
    correo: EmailStr
    observaciones: Optional[str] = None

class SolicitudUpdate(BaseModel):
    quien_tramita: Optional[str] = None
    telefono_principal: Optional[str] = None
    telefono_secundario: Optional[str] = None
    correo: Optional[EmailStr] = None
    observaciones: Optional[str] = None
    estatus: Optional[str] = None
    asunto_id: Optional[int] = None

class CatalogoItem(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
