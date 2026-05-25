from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .base_model import BaseModel

@dataclass
class Bitacora(BaseModel):
    id: Optional[int]
    usuario: str
    accion: str
    detalle: str
    creado_en: Optional[datetime] = None
