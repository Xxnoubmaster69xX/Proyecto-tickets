from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QLabel)
from PyQt6.QtCore import Qt
from .base_view import BaseView
from repositories.bitacora_repository import BitacoraRepository

class BitacoraView(BaseView):
    def __init__(self):
        super().__init__()
        self.repo = BitacoraRepository()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Header Info
        header_layout = QHBoxLayout()
        self.lbl_title = QLabel("Bitácora de Auditoría del Sistema")
        self.lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        
        self.btn_refresh = QPushButton("Refrescar Logs")
        self.btn_refresh.clicked.connect(self.refresh_data)
        
        header_layout.addWidget(self.lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_refresh)
        
        layout.addLayout(header_layout)

        # Logs Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Fecha / Hora", "Usuario", "Acción", "Detalles"])
        
        # Table Styling / Sizing
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)
        self.setLayout(layout)
        self.refresh_data()

    def refresh_data(self):
        logs = self.repo.get_all()
        self.table.setRowCount(0)
        
        for i, log in enumerate(logs):
            self.table.insertRow(i)
            
            # Format datetime
            fecha_str = str(log.creado_en)
            
            self.table.setItem(i, 0, QTableWidgetItem(fecha_str))
            self.table.setItem(i, 1, QTableWidgetItem(log.usuario))
            self.table.setItem(i, 2, QTableWidgetItem(log.accion))
            self.table.setItem(i, 3, QTableWidgetItem(log.detalle))
            
            # Center-align first 3 columns
            for col in range(3):
                item = self.table.item(i, col)
                if item:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
