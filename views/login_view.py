from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from controllers.auth_controller import AuthController

class LoginView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Iniciar Sesión")
        self.setFixedSize(300, 200)
        self.controller = AuthController()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_title = QLabel("Acceso a Administradores")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")

        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Usuario")

        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Contraseña")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.setDefault(True)
        self.btn_login.clicked.connect(self.on_login)

        layout.addWidget(self.lbl_title)
        layout.addWidget(self.txt_username)
        layout.addWidget(self.txt_password)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def on_login(self):
        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()

        if not username or not password:
            QMessageBox.critical(self, "Error", "Por favor ingrese usuario y contraseña.")
            return

        success, msg = self.controller.login(username, password)
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", msg)
