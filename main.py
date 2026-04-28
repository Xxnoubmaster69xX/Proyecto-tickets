import sys
from PyQt6.QtWidgets import QApplication
from database.connection import DatabaseConnection
from views.main_window import MainWindow
from patterns.event_bus import EventBus

def main():
    print("[APP] Iniciando Ticket de Turno...")

    # Inicializar BD
    db = DatabaseConnection()
    db.initialize()
    print("[APP] Base de datos inicializada.")

    # Inicializar aplicación Qt
    app = QApplication(sys.argv)

    # Cargar estilos
    with open("assets/styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    # Mostrar ventana principal
    window = MainWindow()
    window.show()

    # Cleanup al salir
    def on_exit():
        EventBus().clear_all()
        DatabaseConnection().close()
        print("[APP] Aplicación cerrada limpiamente.")

    app.aboutToQuit.connect(on_exit)

    print("[APP] Aplicación lista.")
    sys.exit(app.exec())

    # Agregando el block main para la ejecucion del file.
if __name__ == "__main__":
    main()
