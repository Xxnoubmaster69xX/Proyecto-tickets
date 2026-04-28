from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from .base_view import BaseView
from controllers.dashboard_controller import DashboardController
from controllers.admin_controller import AdminController
from patterns.event_bus import EventBus, AppEvent

class DashboardView(BaseView):
    def __init__(self):
        super().__init__()
        self.controller = DashboardController()
        self.admin_controller = AdminController()
        self.setup_ui()
        self.load_municipios()
        self.refresh_data()
        EventBus().subscribe(AppEvent.ESTATUS_CAMBIADO, lambda _: self.refresh_data())

    def setup_ui(self):
        layout = QVBoxLayout()
        
        top_bar = QHBoxLayout()
        self.cmb_filtro = QComboBox()
        self.cmb_filtro.currentIndexChanged.connect(self.refresh_data)
        
        btn_refresh = QPushButton("Actualizar")
        btn_refresh.clicked.connect(self.refresh_data)
        
        top_bar.addWidget(QLabel("Filtrar por Municipio:"))
        top_bar.addWidget(self.cmb_filtro)
        top_bar.addWidget(btn_refresh)
        
        layout.addLayout(top_bar)
        
        self.kpi_layout = QHBoxLayout()
        self.lbl_total = QLabel("Total: 0")
        self.lbl_pendientes = QLabel("Pendientes: 0")
        self.lbl_resueltas = QLabel("Resueltas: 0")
        self.lbl_pct = QLabel("% Resolución: 0%")
        
        for lbl in (self.lbl_total, self.lbl_pendientes, self.lbl_resueltas, self.lbl_pct):
            lbl.setStyleSheet("font-size: 16px; font-weight: bold; background: white; padding: 10px; border-radius: 5px;")
            self.kpi_layout.addWidget(lbl)
            
        layout.addLayout(self.kpi_layout)
        
        self.figure = Figure(figsize=(10, 5))
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)

    def load_municipios(self):
        self.cmb_filtro.blockSignals(True)
        self.cmb_filtro.clear()
        self.cmb_filtro.addItem("Todos", None)
        for m in self.admin_controller.get_municipios():
            self.cmb_filtro.addItem(m.nombre, m.id)
        self.cmb_filtro.blockSignals(False)

    def refresh_data(self):
        m_id = self.cmb_filtro.currentData()
        stats = self.controller.get_stats(m_id)
        
        total = stats['total']
        resueltos = stats['resueltos']
        pct = (resueltos / total * 100) if total > 0 else 0
        
        self.lbl_total.setText(f"Total: {total}")
        self.lbl_pendientes.setText(f"Pendientes: {stats['pendientes']}")
        self.lbl_resueltas.setText(f"Resueltas: {resueltos}")
        self.lbl_pct.setText(f"% Resolución: {pct:.1f}%")
        
        self.draw_charts(stats, bool(m_id))

    def draw_charts(self, stats: dict, is_filtered: bool):
        self.figure.clear()
        
        ax1 = self.figure.add_subplot(121)
        labels = ['Pendientes', 'Resueltos']
        sizes = [stats['pendientes'], stats['resueltos']]
        colors = ['#f39c12', '#27ae60']
        
        if sum(sizes) == 0:
            ax1.text(0.5, 0.5, "Sin datos", ha="center", va="center")
        else:
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
        ax1.set_title("Estatus de Solicitudes")

        ax2 = self.figure.add_subplot(122)
        if is_filtered:
            # Mostrar por asunto
            data = stats['por_asunto']
            if not data:
                ax2.text(0.5, 0.5, "Sin datos", ha="center", va="center")
            else:
                y_pos = range(len(data))
                names = [d[0] for d in data]
                counts = [d[1] for d in data]
                ax2.barh(y_pos, counts, align='center', color='#3498db')
                ax2.set_yticks(y_pos, labels=names)
                ax2.invert_yaxis()  
                ax2.set_title("Por Asunto")
        else:
            # Mostrar por municipio (top 10)
            data = sorted(stats['por_municipio'], key=lambda x: x[1], reverse=True)[:10]
            if not data:
                ax2.text(0.5, 0.5, "Sin datos", ha="center", va="center")
            else:
                y_pos = range(len(data))
                names = [d[0] for d in data]
                counts = [d[1] for d in data]
                ax2.barh(y_pos, counts, align='center', color='#9b59b6')
                ax2.set_yticks(y_pos, labels=names)
                ax2.invert_yaxis()
                ax2.set_title("Top 10 Municipios")
                
        self.figure.tight_layout()
        self.canvas.draw()
