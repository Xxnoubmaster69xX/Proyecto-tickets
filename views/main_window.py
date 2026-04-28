from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QApplication
from PyQt6.QtGui import QAction
from utils.session_manager import SessionManager
from controllers.auth_controller import AuthController
from patterns.event_bus import EventBus, AppEvent

from .login_view import LoginView
from .solicitud_publica_view import SolicitudPublicaView
from .busqueda_view import BusquedaView
from .catalogos_view import CatalogosView
from .dashboard_view import DashboardView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ticket de Turno")
        self.resize(1024, 768)
        self.auth_controller = AuthController()
        
        self.setup_ui()
        self.update_menu_state()
        
        EventBus().subscribe(AppEvent.LOGIN_EXITOSO, self.on_login_state_changed)
        EventBus().subscribe(AppEvent.LOGOUT, self.on_login_state_changed)

    def setup_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.view_publica = SolicitudPublicaView()
        self.view_busqueda = BusquedaView()
        self.view_catalogos = CatalogosView()
        self.view_dashboard = DashboardView()
        
        self.stacked_widget.addWidget(self.view_publica)
        self.stacked_widget.addWidget(self.view_busqueda)
        self.stacked_widget.addWidget(self.view_catalogos)
        self.stacked_widget.addWidget(self.view_dashboard)
        
        self.create_menus()
        self.statusBar().showMessage("Modo Público")

    def create_menus(self):
        menubar = self.menuBar()
        
        # Archivo
        menu_archivo = menubar.addMenu("Sistema")
        self.action_login = QAction("Iniciar Sesión", self)
        self.action_login.triggered.connect(self.show_login)
        self.action_logout = QAction("Cerrar Sesión", self)
        self.action_logout.triggered.connect(self.do_logout)
        action_salir = QAction("Salir", self)
        action_salir.triggered.connect(self.close)
        
        menu_archivo.addAction(self.action_login)
        menu_archivo.addAction(self.action_logout)
        menu_archivo.addSeparator()
        menu_archivo.addAction(action_salir)
        
        # Solicitudes
        menu_solicitudes = menubar.addMenu("Tramites")
        action_registrar = QAction("Registrar / Modificar Solicitud", self)
        action_registrar.triggered.connect(lambda: self.switch_view(self.view_publica))
        menu_solicitudes.addAction(action_registrar)
        
        # Administración
        self.menu_admin = menubar.addMenu("Administración")
        action_buscar = QAction("Búsqueda de Solicitudes", self)
        action_buscar.triggered.connect(lambda: self.switch_view(self.view_busqueda))
        action_catalogos = QAction("Catálogos", self)
        action_catalogos.triggered.connect(lambda: self.switch_view(self.view_catalogos))
        action_dashboard = QAction("Dashboard e Informes", self)
        action_dashboard.triggered.connect(lambda: self.switch_view(self.view_dashboard))
        
        self.menu_admin.addAction(action_buscar)
        self.menu_admin.addAction(action_catalogos)
        self.menu_admin.addAction(action_dashboard)

    def update_menu_state(self):
        is_auth = SessionManager().is_authenticated
        self.action_login.setVisible(not is_auth)
        self.action_logout.setVisible(bool(is_auth))
        self.menu_admin.menuAction().setVisible(bool(is_auth))
        
        if is_auth:
            user = SessionManager().current_user
            self.statusBar().showMessage(f"Sesión activa: {user.username} - {user.nombre_completo}")
        else:
            self.statusBar().showMessage("Modo Público")
            self.switch_view(self.view_publica)

    def show_login(self):
        dialog = LoginView(self)
        if dialog.exec():
            # El estado se actualiza por el evento
            pass

    def do_logout(self):
        self.auth_controller.logout()
        
    def on_login_state_changed(self, data):
        self.update_menu_state()

    def switch_view(self, view):
        self.stacked_widget.setCurrentWidget(view)
        
    def closeEvent(self, event):
        QApplication.quit()
