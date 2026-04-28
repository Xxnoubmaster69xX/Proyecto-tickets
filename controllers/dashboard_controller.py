from typing import Optional
from repositories.solicitud_repository import SolicitudRepository

class DashboardController:
    def __init__(self):
        self.repo = SolicitudRepository()

    def get_stats(self, municipio_id: Optional[int] = None) -> dict:
        return self.repo.get_stats_by_municipio(municipio_id)
