from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import io
import os
from models.solicitud import Solicitud
from datetime import datetime

def generate_ticket_pdf(solicitud: Solicitud) -> bytes:
    """
    Genera el PDF del comprobante de turno usando Canvas puro para máximo control gráfico.
    Estética Dark Mode / Liquid Glass garantizada en 1 sola página.
    """
    buffer = io.BytesIO()
    
    # 612 x 792 points (Letter size)
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # 1. Fondo Oscuro
    c.setFillColor(HexColor('#0f172a'))
    c.rect(0, 0, width, height, fill=True, stroke=False)
    
    # 2. Logo
    logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public', 'logo.webp'))
    if os.path.exists(logo_path):
        # Center logo: width 100, height 100
        c.drawImage(logo_path, (width - 100) / 2, height - 140, width=100, height=100, mask='auto')
    
    # 3. Encabezados
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(HexColor('#f8fafc'))
    c.drawCentredString(width / 2, height - 180, "TICKET DE TURNO ESCOLAR")
    
    c.setFont("Helvetica", 11)
    c.setFillColor(HexColor('#60a5fa'))
    c.drawCentredString(width / 2, height - 200, "SISTEMA DE GESTIÓN Y ATENCIÓN CIUDADANA - UADEC")
    
    # 4. Número de Turno Gigante
    c.setFont("Helvetica-Bold", 54)
    c.setFillColor(HexColor('#3b82f6'))
    c.drawCentredString(width / 2, height - 280, f"#{solicitud.numero_turno:04d}")
    
    # 5. Tarjeta de Datos (Rounded Box)
    box_x = 40
    box_y = 150
    box_w = width - 80
    box_h = 320
    
    c.setFillColor(HexColor('#1e293b'))
    c.setStrokeColor(HexColor('#334155'))
    c.setLineWidth(1)
    c.roundRect(box_x, box_y, box_w, box_h, 15, fill=True, stroke=True)
    
    # 6. Contenido de la Tarjeta
    y_cursor = box_y + box_h - 35
    col1_x = 65
    col2_x = 320
    
    # -- Sección 1: Datos del Alumno --
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(HexColor('#3b82f6'))
    c.drawString(col1_x, y_cursor, "DATOS DEL ALUMNO")
    
    y_cursor -= 25
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(HexColor('#94a3b8'))
    c.drawString(col1_x, y_cursor, "CURP Registrada:")
    c.drawString(col2_x, y_cursor, "Municipio Asignado:")
    
    y_cursor -= 18
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor('#f8fafc'))
    c.drawString(col1_x, y_cursor, solicitud.curp_alumno)
    c.drawString(col2_x, y_cursor, solicitud.municipio_nombre or "N/A")
    
    y_cursor -= 25
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(HexColor('#94a3b8'))
    c.drawString(col1_x, y_cursor, "Nombre Completo:")
    
    y_cursor -= 18
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor('#f8fafc'))
    c.drawString(col1_x, y_cursor, solicitud.nombre_alumno or "Pendiente de validación")
    
    y_cursor -= 30
    # Línea Divisoria
    c.setStrokeColor(HexColor('#334155'))
    c.line(box_x, y_cursor, box_x + box_w, y_cursor)
    
    y_cursor -= 30
    # -- Sección 2: Trámite y Contacto --
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(HexColor('#3b82f6'))
    c.drawString(col1_x, y_cursor, "DATOS DEL TRÁMITE Y CONTACTO")
    
    y_cursor -= 25
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(HexColor('#94a3b8'))
    c.drawString(col1_x, y_cursor, "Asunto a Tratar:")
    c.drawString(col2_x, y_cursor, "Estatus Actual:")
    
    y_cursor -= 18
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor('#f8fafc'))
    c.drawString(col1_x, y_cursor, solicitud.asunto_descripcion or "N/A")
    
    if solicitud.estatus.lower() == 'pendiente':
        c.setFillColor(HexColor('#fbbf24')) # Amarillo
    else:
        c.setFillColor(HexColor('#34d399')) # Verde
    c.drawString(col2_x, y_cursor, solicitud.estatus.upper())
    
    y_cursor -= 25
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(HexColor('#94a3b8'))
    c.drawString(col1_x, y_cursor, "Tutor Responsable:")
    c.drawString(col2_x, y_cursor, "Teléfono Principal:")
    
    y_cursor -= 18
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor('#f8fafc'))
    c.drawString(col1_x, y_cursor, solicitud.quien_tramita)
    c.drawString(col2_x, y_cursor, solicitud.telefono_principal)
    
    y_cursor -= 25
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(HexColor('#94a3b8'))
    c.drawString(col1_x, y_cursor, "Correo Electrónico:")
    c.drawString(col2_x, y_cursor, "Fecha de Emisión:")
    
    y_cursor -= 18
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor('#f8fafc'))
    c.drawString(col1_x, y_cursor, solicitud.correo)
    c.drawString(col2_x, y_cursor, datetime.now().strftime("%d/%m/%Y %H:%M"))
    
    # 7. Footer
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(HexColor('#94a3b8'))
    c.drawCentredString(width / 2, 80, "Por favor, presente este comprobante digital o impreso el día de su cita.")
    c.drawCentredString(width / 2, 65, "Este documento garantiza su lugar de atención según el municipio correspondiente.")
    
    # Finalizar página
    c.showPage()
    c.save()
    
    return buffer.getvalue()
