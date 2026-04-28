from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .base_model import BaseModel

@dataclass
class Usuario(BaseModel):
    id: Optional[int]
    username: str
    password_hash: str
    nombre_completo: str
    activo: int = 1
    creado_en: Optional[datetime] = None
