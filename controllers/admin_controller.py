from repositories.catalogo_repository import CatalogoRepository
from patterns.event_bus import EventBus, AppEvent

class AdminController:
    def __init__(self):
        self.repo = CatalogoRepository()

    def get_municipios(self):
        return self.repo.get_municipios()

    def get_niveles(self):
        return self.repo.get_niveles()

    def get_asuntos(self):
        return self.repo.get_asuntos()

    def create_catalogo(self, tipo: str, valor: str) -> bool:
        res = False
        if tipo == 'municipio':
            res = self.repo.create_municipio(valor)
        elif tipo == 'nivel':
            res = self.repo.create_nivel(valor)
        elif tipo == 'asunto':
            res = self.repo.create_asunto(valor)
        
        if res:
            EventBus().publish(AppEvent.CATALOGO_ACTUALIZADO, tipo)
        return res

    def update_catalogo(self, tipo: str, id: int, valor: str) -> bool:
        res = False
        if tipo == 'municipio':
            res = self.repo.update_municipio(id, valor)
        elif tipo == 'nivel':
            res = self.repo.update_nivel(id, valor)
        elif tipo == 'asunto':
            res = self.repo.update_asunto(id, valor)
            
        if res:
            EventBus().publish(AppEvent.CATALOGO_ACTUALIZADO, tipo)
        return res

    def delete_catalogo(self, tipo: str, id: int) -> bool:
        res = False
        if tipo == 'municipio':
            res = self.repo.delete_municipio(id)
        elif tipo == 'nivel':
            res = self.repo.delete_nivel(id)
        elif tipo == 'asunto':
            res = self.repo.delete_asunto(id)
            
        if res:
            EventBus().publish(AppEvent.CATALOGO_ACTUALIZADO, tipo)
        return res
