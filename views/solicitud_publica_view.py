from PyQt6.QtWidgets import (QFormLayout, QVBoxLayout, QLineEdit, QComboBox, 
                             QPushButton, QTextEdit, QHBoxLayout, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt
from .base_view import BaseView
from controllers.solicitud_controller import SolicitudController
from controllers.admin_controller import AdminController
from utils.curp_validator import validate_curp
from utils.ticket_generator import generate_ticket_pdf
from patterns.event_bus import EventBus, AppEvent

class SolicitudPublicaView(BaseView):
    def __init__(self, registro_only=False):
        self.registro_only = registro_only
        super().__init__()
        self.controller = SolicitudController()
        self.admin_controller = AdminController()
        self.setup_ui()
        self.load_catalogs()
        
        EventBus().subscribe(AppEvent.CATALOGO_ACTUALIZADO, lambda x: self.load_catalogs())

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        form_layout = QFormLayout()

        # Fields
        self.txt_curp = QLineEdit()
        self.txt_curp.textChanged.connect(self.on_curp_changed)
        self.txt_nombre = QLineEdit()
        self.txt_paterno = QLineEdit()
        self.txt_materno = QLineEdit()
        
        self.cmb_nivel = QComboBox()
        self.cmb_municipio = QComboBox()
        
        self.txt_quien = QLineEdit()
        self.txt_tel1 = QLineEdit()
        self.txt_tel2 = QLineEdit()
        self.txt_correo = QLineEdit()
        
        self.cmb_asunto = QComboBox()
        self.txt_observaciones = QTextEdit()
        self.txt_observaciones.setMaximumHeight(80)

        # Modificación
        self.txt_turno_mod = QLineEdit()
        self.txt_turno_mod.setPlaceholderText("Nº Turno (Solo para modificar)")
        self.btn_buscar_mod = QPushButton("Buscar por CURP + Turno")
        self.btn_buscar_mod.clicked.connect(self.buscar_para_modificar)

        if not self.registro_only:
            mod_layout = QHBoxLayout()
            mod_layout.addWidget(self.txt_turno_mod)
            mod_layout.addWidget(self.btn_buscar_mod)
            form_layout.addRow("Modificar Trámite:", mod_layout)

        form_layout.addRow("CURP Alumno *", self.txt_curp)
        form_layout.addRow("Nombre *", self.txt_nombre)
        form_layout.addRow("Apellido Paterno *", self.txt_paterno)
        form_layout.addRow("Apellido Materno *", self.txt_materno)
        form_layout.addRow("Nivel Educativo *", self.cmb_nivel)
        form_layout.addRow("Municipio *", self.cmb_municipio)
        form_layout.addRow("Trámite / Asunto *", self.cmb_asunto)
        form_layout.addRow("Quien realiza el trámite *", self.txt_quien)
        form_layout.addRow("Teléfono Principal *", self.txt_tel1)
        form_layout.addRow("Teléfono Secundario", self.txt_tel2)
        form_layout.addRow("Correo Electrónico *", self.txt_correo)
        form_layout.addRow("Observaciones", self.txt_observaciones)

        self.btn_guardar = QPushButton("Registrar Solicitud")
        self.btn_guardar.setDefault(True)
        self.btn_guardar.clicked.connect(self.guardar)

        layout.addLayout(form_layout)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def load_catalogs(self):
        self.cmb_municipio.clear()
        self.cmb_nivel.clear()
        self.cmb_asunto.clear()
        
        for m in self.admin_controller.get_municipios():
            self.cmb_municipio.addItem(m.nombre, m.id)
            
        for n in self.admin_controller.get_niveles():
            self.cmb_nivel.addItem(n.nombre, n.id)
            
        for a in self.admin_controller.get_asuntos():
            self.cmb_asunto.addItem(a.descripcion, a.id)

    def on_curp_changed(self):
        curp = self.txt_curp.text().upper()
        if len(curp) == 18:
            is_valid, _ = validate_curp(curp)
            self.txt_curp.setProperty("valid", is_valid)
            self.txt_curp.style().unpolish(self.txt_curp)
            self.txt_curp.style().polish(self.txt_curp)

    def buscar_para_modificar(self):
        curp = self.txt_curp.text().strip()
        turno = self.txt_turno_mod.text().strip()
        if not curp or not turno.isdigit():
            self.show_error("Debe ingresar la CURP y el Número de Turno para modificar.")
            return

        sol = self.controller.buscar_por_turno_y_curp(int(turno), curp)
        if sol:
            self.txt_quien.setText(sol.quien_tramita)
            self.txt_tel1.setText(sol.telefono_principal)
            self.txt_tel2.setText(sol.telefono_secundario or "")
            self.txt_correo.setText(sol.correo)
            self.txt_observaciones.setText(sol.observaciones or "")
            
            # Select combos
            idx = self.cmb_asunto.findData(sol.asunto_id)
            if idx >= 0: self.cmb_asunto.setCurrentIndex(idx)
            
            idx = self.cmb_municipio.findData(sol.municipio_id)
            if idx >= 0: self.cmb_municipio.setCurrentIndex(idx)
            
            self.txt_nombre.setDisabled(True)
            self.txt_paterno.setDisabled(True)
            self.txt_materno.setDisabled(True)
            self.cmb_nivel.setDisabled(True)
            self.cmb_municipio.setDisabled(True)
            
            self.btn_guardar.setText("Guardar Modificaciones")
            self.show_info("Solicitud encontrada. Puede modificar los datos de contacto y asunto.")
        else:
            self.show_error("No se encontró solicitud con esos datos.")

    def guardar(self):
        datos = {
            'curp_alumno': self.txt_curp.text().strip(),
            'nombre': self.txt_nombre.text().strip(),
            'paterno': self.txt_paterno.text().strip(),
            'materno': self.txt_materno.text().strip(),
            'nivel_id': self.cmb_nivel.currentData(),
            'municipio_id': self.cmb_municipio.currentData(),
            'asunto_id': self.cmb_asunto.currentData(),
            'quien_tramita': self.txt_quien.text().strip(),
            'telefono_principal': self.txt_tel1.text().strip(),
            'telefono_secundario': self.txt_tel2.text().strip(),
            'correo': self.txt_correo.text().strip(),
            'observaciones': self.txt_observaciones.toPlainText().strip()
        }

        turno_mod = self.txt_turno_mod.text().strip()
        
        if turno_mod.isdigit():
            # Modo modificar
            success, msg = self.controller.modificar_solicitud(datos['curp_alumno'], int(turno_mod), datos)
            if success:
                self.show_info("Solicitud actualizada exitosamente.")
                self.reset_form()
            else:
                self.show_error(msg)
        else:
            # Modo registro
            success, msg, solicitud = self.controller.registrar_solicitud(datos)
            if success:
                self.show_info(f"Solicitud registrada. Su turno es: {solicitud.numero_turno}", "Éxito")
                
                resp = QMessageBox.question(self, "PDF", "¿Desea descargar el comprobante PDF?", 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if resp == QMessageBox.StandardButton.Yes:
                    self.descargar_pdf(solicitud)
                self.reset_form()
            else:
                self.show_error(msg)

    def descargar_pdf(self, solicitud):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Comprobante", 
                                              f"Turno_{solicitud.numero_turno}_{solicitud.curp_alumno}.pdf", 
                                              "PDF Files (*.pdf)")
        if path:
            try:
                pdf_bytes = generate_ticket_pdf(solicitud)
                with open(path, "wb") as f:
                    f.write(pdf_bytes)
                self.show_info("PDF guardado correctamente.")
            except Exception as e:
                self.show_error(f"No se pudo guardar el archivo: {e}")

    def reset_form(self):
        self.txt_curp.clear()
        self.txt_nombre.clear()
        self.txt_paterno.clear()
        self.txt_materno.clear()
        self.txt_quien.clear()
        self.txt_tel1.clear()
        self.txt_tel2.clear()
        self.txt_correo.clear()
        self.txt_observaciones.clear()
        self.txt_turno_mod.clear()
        
        self.txt_nombre.setEnabled(True)
        self.txt_paterno.setEnabled(True)
        self.txt_materno.setEnabled(True)
        self.cmb_nivel.setEnabled(True)
        self.cmb_municipio.setEnabled(True)
        self.btn_guardar.setText("Registrar Solicitud")
