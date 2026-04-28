from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .base_model import BaseModel

@dataclass
class Solicitud(BaseModel):
    id: Optional[int]
    numero_turno: int
    curp_alumno: str
    quien_tramita: str
    telefono_principal: str
    telefono_secundario: Optional[str]
    correo: str
    asunto_id: int
    municipio_id: int
    estatus: str
    observaciones: Optional[str]
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None
    
    # Extractos de joins
    nombre_alumno: Optional[str] = None
    municipio_nombre: Optional[str] = None
    asunto_descripcion: Optional[str] = None
