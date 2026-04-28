from PyQt6.QtWidgets import QWidget, QMessageBox

class BaseView(QWidget):
    def show_error(self, message: str, title: str = "Error"):
        QMessageBox.critical(self, title, message)

    def show_info(self, message: str, title: str = "Información"):
        QMessageBox.information(self, title, message)

    def show_warning(self, message: str, title: str = "Advertencia"):
        QMessageBox.warning(self, title, message)
