from dataclasses import dataclass
from typing import Optional
from .base_model import BaseModel

@dataclass
class Municipio(BaseModel):
    id: Optional[int]
    nombre: str
    activo: int = 1
