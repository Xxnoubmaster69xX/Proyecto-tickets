import dataclasses
from typing import Any, Dict

class BaseModel:
    """Clase base abstracta para todos los modelos."""
    
    def to_dict(self) -> Dict[str, Any]:
        if dataclasses.is_dataclass(self):
            return dataclasses.asdict(self)
        return vars(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_dict()})"
