from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox)
from .base_view import BaseView
from controllers.solicitud_controller import SolicitudController
from .admin_crud_view import AdminCrudView

class BusquedaView(BaseView):
    def __init__(self):
        super().__init__()
        self.controller = SolicitudController()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.tab_curp = QWidget()
        self.tab_nombre = QWidget()
        
        self.setup_tab_curp()
        self.setup_tab_nombre()
        
        self.tabs.addTab(self.tab_curp, "Buscar por CURP")
        self.tabs.addTab(self.tab_nombre, "Buscar por Nombre")
        
        layout.addWidget(self.tabs)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Turno", "CURP", "Nombre Alumno", "Municipio", "Asunto", "Estatus", "Fecha"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemDoubleClicked.connect(self.on_double_click)
        
        layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        self.btn_modificar = QPushButton("Modificar")
        self.btn_estatus = QPushButton("Cambiar Estatus")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setObjectName("btnDanger")
        
        self.btn_modificar.clicked.connect(self.modificar_seleccion)
        self.btn_estatus.clicked.connect(self.cambiar_estatus_seleccion)
        self.btn_eliminar.clicked.connect(self.eliminar_seleccion)
        
        btn_layout.addWidget(self.btn_modificar)
        btn_layout.addWidget(self.btn_estatus)
        btn_layout.addWidget(self.btn_eliminar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def setup_tab_curp(self):
        layout = QHBoxLayout()
        self.txt_curp = QLineEdit()
        self.txt_curp.setPlaceholderText("Ingrese CURP")
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(lambda: self.buscar("curp"))
        layout.addWidget(self.txt_curp)
        layout.addWidget(btn_buscar)
        self.tab_curp.setLayout(layout)

    def setup_tab_nombre(self):
        layout = QHBoxLayout()
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Ingrese nombre, paterno o materno")
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(lambda: self.buscar("nombre"))
        layout.addWidget(self.txt_nombre)
        layout.addWidget(btn_buscar)
        self.tab_nombre.setLayout(layout)

    def buscar(self, criterio: str):
        resultados = []
        if criterio == "curp":
            resultados = self.controller.buscar_por_curp(self.txt_curp.text())
        else:
            resultados = self.controller.buscar_por_nombre(self.txt_nombre.text())
            
        self.table.setRowCount(0)
        self.solicitudes_actuales = resultados
        
        for i, sol in enumerate(resultados):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(sol.numero_turno)))
            self.table.setItem(i, 1, QTableWidgetItem(sol.curp_alumno))
            self.table.setItem(i, 2, QTableWidgetItem(sol.nombre_alumno))
            self.table.setItem(i, 3, QTableWidgetItem(sol.municipio_nombre))
            self.table.setItem(i, 4, QTableWidgetItem(sol.asunto_descripcion))
            self.table.setItem(i, 5, QTableWidgetItem(sol.estatus))
            self.table.setItem(i, 6, QTableWidgetItem(str(sol.creado_en)[:10] if sol.creado_en else ""))

    def get_selected_solicitud(self):
        row = self.table.currentRow()
        if row >= 0 and row < len(self.solicitudes_actuales):
            return self.solicitudes_actuales[row]
        return None

    def on_double_click(self, item):
        self.modificar_seleccion()

    def modificar_seleccion(self):
        sol = self.get_selected_solicitud()
        if not sol:
            self.show_error("Debe seleccionar una solicitud.")
            return
            
        dialog = AdminCrudView(sol)
        if dialog.exec():
            # Refresh
            if self.tabs.currentIndex() == 0:
                self.buscar("curp")
            else:
                self.buscar("nombre")

    def cambiar_estatus_seleccion(self):
        sol = self.get_selected_solicitud()
        if not sol:
            self.show_error("Debe seleccionar una solicitud.")
            return
            
        nuevo_estatus = "Resuelto" if sol.estatus == "Pendiente" else "Pendiente"
        resp = QMessageBox.question(self, "Cambiar estatus", 
                                   f"¿Cambiar estatus a '{nuevo_estatus}'?")
        if resp == QMessageBox.StandardButton.Yes:
            success, msg = self.controller.cambiar_estatus(sol.id, nuevo_estatus)
            if success:
                self.show_info("Estatus cambiado.")
                if self.tabs.currentIndex() == 0: self.buscar("curp")
                else: self.buscar("nombre")
            else:
                self.show_error(msg)

    def eliminar_seleccion(self):
        sol = self.get_selected_solicitud()
        if not sol:
            self.show_error("Debe seleccionar una solicitud.")
            return
            
        resp = QMessageBox.question(self, "Eliminar", 
                                   "¿Está seguro de eliminar esta solicitud de forma permanente?")
        if resp == QMessageBox.StandardButton.Yes:
            success, msg = self.controller.eliminar_solicitud(sol.id)
            if success:
                self.show_info("Solicitud eliminada.")
                if self.tabs.currentIndex() == 0: self.buscar("curp")
                else: self.buscar("nombre")
            else:
                self.show_error(msg)
