from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog, QMessageBox)
from .base_view import BaseView
from controllers.admin_controller import AdminController

class CatalogosView(BaseView):
    def __init__(self):
        super().__init__()
        self.controller = AdminController()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        
        self.tab_municipios = self.create_tab("municipio", self.controller.get_municipios)
        self.tab_niveles = self.create_tab("nivel", self.controller.get_niveles)
        self.tab_asuntos = self.create_tab("asunto", self.controller.get_asuntos)
        
        self.tabs.addTab(self.tab_municipios, "Municipios")
        self.tabs.addTab(self.tab_niveles, "Niveles Educativos")
        self.tabs.addTab(self.tab_asuntos, "Asuntos")
        
        self.tabs.currentChanged.connect(self.refresh_current_tab)
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        
    def create_tab(self, tipo: str, fetch_method):
        tab = QWidget()
        layout = QVBoxLayout()
        
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["ID", "Nombre/Descripción"])
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        setattr(self, f"table_{tipo}", table)
        
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Agregar")
        btn_edit = QPushButton("Editar")
        btn_del = QPushButton("Eliminar")
        btn_del.setObjectName("btnDanger")
        
        btn_add.clicked.connect(lambda: self.add_item(tipo))
        btn_edit.clicked.connect(lambda: self.edit_item(tipo))
        btn_del.clicked.connect(lambda: self.del_item(tipo))
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_del)
        
        layout.addWidget(table)
        layout.addLayout(btn_layout)
        tab.setLayout(layout)
        
        self.populate_table(tipo, fetch_method())
        return tab

    def populate_table(self, tipo: str, items):
        table = getattr(self, f"table_{tipo}")
        table.setRowCount(0)
        setattr(self, f"data_{tipo}", items)
        
        for i, item in enumerate(items):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(str(item.id)))
            
            # handle field names
            val = item.nombre if hasattr(item, 'nombre') else item.descripcion
            table.setItem(i, 1, QTableWidgetItem(val))

    def refresh_current_tab(self):
        idx = self.tabs.currentIndex()
        if idx == 0: self.populate_table("municipio", self.controller.get_municipios())
        elif idx == 1: self.populate_table("nivel", self.controller.get_niveles())
        elif idx == 2: self.populate_table("asunto", self.controller.get_asuntos())

    def get_selected(self, tipo: str):
        table = getattr(self, f"table_{tipo}")
        idx = table.currentRow()
        data = getattr(self, f"data_{tipo}", [])
        if idx >= 0 and idx < len(data):
            return data[idx]
        return None

    def add_item(self, tipo: str):
        text, ok = QInputDialog.getText(self, f"Agregar {tipo}", "Ingrese nombre/descripción:")
        if ok and text.strip():
            if self.controller.create_catalogo(tipo, text.strip()):
                self.refresh_current_tab()
            else:
                self.show_error("Error al crear el registro.")

    def edit_item(self, tipo: str):
        item = self.get_selected(tipo)
        if not item:
            self.show_error("Seleccione un registro.")
            return
            
        current_val = item.nombre if hasattr(item, 'nombre') else item.descripcion
        text, ok = QInputDialog.getText(self, f"Editar {tipo}", "Edite nombre/descripción:", QLineEdit.EchoMode.Normal, current_val)
        if ok and text.strip():
            if self.controller.update_catalogo(tipo, item.id, text.strip()):
                self.refresh_current_tab()
            else:
                self.show_error("Error al actualizar el registro.")

    def del_item(self, tipo: str):
        item = self.get_selected(tipo)
        if not item:
            self.show_error("Seleccione un registro.")
            return
            
        resp = QMessageBox.question(self, "Eliminar", "¿Dar de baja este registro?")
        if resp == QMessageBox.StandardButton.Yes:
            if self.controller.delete_catalogo(tipo, item.id):
                self.refresh_current_tab()
            else:
                self.show_error("No se puede eliminar (probablemente hay registros dependientes o un error).")
