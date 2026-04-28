from dataclasses import dataclass
from .base_model import BaseModel

@dataclass
class Alumno(BaseModel):
    curp: str
    nombre: str
    paterno: str
    materno: str
    nivel_id: int
    municipio_id: int

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.paterno} {self.materno}"
