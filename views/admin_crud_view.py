from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QComboBox, QTextEdit, QPushButton, QHBoxLayout, QMessageBox)
from controllers.solicitud_controller import SolicitudController
from controllers.admin_controller import AdminController
from models.solicitud import Solicitud

class AdminCrudView(QDialog):
    def __init__(self, solicitud: Solicitud, parent=None):
        super().__init__(parent)
        self.solicitud = solicitud
        self.controller = SolicitudController()
        self.admin_controller = AdminController()
        self.setWindowTitle(f"Editando Solicitud: {solicitud.curp_alumno} - Turno {solicitud.numero_turno}")
        self.setMinimumWidth(500)
        self.setup_ui()
        self.populate_data()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.txt_quien = QLineEdit()
        self.txt_tel1 = QLineEdit()
        self.txt_tel2 = QLineEdit()
        self.txt_correo = QLineEdit()
        
        self.cmb_asunto = QComboBox()
        self.cmb_municipio = QComboBox()
        # admin allows changing status
        self.cmb_estatus = QComboBox()
        self.cmb_estatus.addItems(["Pendiente", "Resuelto"])
        
        self.txt_observaciones = QTextEdit()
        
        form_layout.addRow("Quien tramita", self.txt_quien)
        form_layout.addRow("Teléfono 1", self.txt_tel1)
        form_layout.addRow("Teléfono 2", self.txt_tel2)
        form_layout.addRow("Correo", self.txt_correo)
        form_layout.addRow("Asunto", self.cmb_asunto)
        form_layout.addRow("Municipio", self.cmb_municipio)
        form_layout.addRow("Estatus", self.cmb_estatus)
        form_layout.addRow("Observaciones", self.txt_observaciones)
        
        for m in self.admin_controller.get_municipios():
            self.cmb_municipio.addItem(m.nombre, m.id)
            
        for a in self.admin_controller.get_asuntos():
            self.cmb_asunto.addItem(a.descripcion, a.id)
            
        layout.addLayout(form_layout)
        
        btn_box = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_cancelar = QPushButton("Cancelar")
        btn_guardar.clicked.connect(self.guardar)
        btn_cancelar.clicked.connect(self.reject)
        btn_box.addWidget(btn_guardar)
        btn_box.addWidget(btn_cancelar)
        
        layout.addLayout(btn_box)
        self.setLayout(layout)

    def populate_data(self):
        self.txt_quien.setText(self.solicitud.quien_tramita)
        self.txt_tel1.setText(self.solicitud.telefono_principal)
        self.txt_tel2.setText(self.solicitud.telefono_secundario or "")
        self.txt_correo.setText(self.solicitud.correo)
        self.txt_observaciones.setText(self.solicitud.observaciones or "")
        
        # combos
        idx = self.cmb_estatus.findText(self.solicitud.estatus)
        if idx >= 0: self.cmb_estatus.setCurrentIndex(idx)
        
        idx = self.cmb_municipio.findData(self.solicitud.municipio_id)
        if idx >= 0: self.cmb_municipio.setCurrentIndex(idx)
        
        idx = self.cmb_asunto.findData(self.solicitud.asunto_id)
        if idx >= 0: self.cmb_asunto.setCurrentIndex(idx)

    def guardar(self):
        datos = {
            'quien_tramita': self.txt_quien.text().strip(),
            'telefono_principal': self.txt_tel1.text().strip(),
            'telefono_secundario': self.txt_tel2.text().strip(),
            'correo': self.txt_correo.text().strip(),
            'observaciones': self.txt_observaciones.toPlainText().strip(),
            'estatus': self.cmb_estatus.currentText(),
            'asunto_id': self.cmb_asunto.currentData(),
            'municipio_id': self.cmb_municipio.currentData()
        }
        
        success, msg = self.controller.modificar_solicitud(self.solicitud.curp_alumno, self.solicitud.numero_turno, datos)
        if success:
            QMessageBox.information(self, "Éxito", "Solicitud guardada correctamente.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", msg)
