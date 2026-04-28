from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """
    Interface genérica del patrón Repository.
    Define el contrato CRUD que todos los repositorios deben cumplir.
    """

    @abstractmethod
    def get_by_id(self, id) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, entity: T) -> bool:
        pass

    @abstractmethod
    def delete(self, id) -> bool:
        pass
