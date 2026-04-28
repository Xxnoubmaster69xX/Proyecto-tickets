from dataclasses import dataclass
from typing import Optional
from .base_model import BaseModel

@dataclass
class Asunto(BaseModel):
    id: Optional[int]
    descripcion: str
    activo: int = 1
