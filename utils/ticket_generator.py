from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import io
from models.solicitud import Solicitud
from datetime import datetime

def generate_ticket_pdf(solicitud: Solicitud) -> bytes:
    """
    Genera el PDF del comprobante de turno.
    Returns: bytes del PDF listo para guardar o imprimir.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('Title', fontSize=20, fontName='Helvetica-Bold', textColor=HexColor('#1a5276'), spaceAfter=10, alignment=1)
    turno_style = ParagraphStyle('Turno', fontSize=32, fontName='Helvetica-Bold', textColor=HexColor('#e74c3c'), alignment=1, spaceAfter=20)
    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.spaceAfter = 8

    elements.append(Paragraph("Comprobante de Turno — Ticket de Turno Escolar", title_style))
    elements.append(Paragraph(f"TURNO #{solicitud.numero_turno:04d}", turno_style))

    data = [
        ["Datos del Alumno", ""],
        ["CURP:", solicitud.curp_alumno],
        ["Nombre:", solicitud.nombre_alumno or ""],
        ["Municipio:", solicitud.municipio_nombre or ""],
        ["", ""],
        ["Datos del Trámite", ""],
        ["Asunto:", solicitud.asunto_descripcion or ""],
        ["Quien tramita:", solicitud.quien_tramita],
        ["Teléfono:", solicitud.telefono_principal],
        ["Correo:", solicitud.correo],
        ["Fecha de Registro:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]

    t = Table(data, colWidths=[150, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), HexColor('#2980b9')),
        ('TEXTCOLOR', (0, 0), (1, 0), HexColor('#ffffff')),
        ('BACKGROUND', (0, 5), (1, 5), HexColor('#2980b9')),
        ('TEXTCOLOR', (0, 5), (1, 5), HexColor('#ffffff')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 5), (1, 5), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("Presente este comprobante el día de su cita", ParagraphStyle('FooterMsg', fontSize=14, fontName='Helvetica-Oblique', alignment=1)))
    elements.append(Paragraph(f"Turno: {solicitud.numero_turno:04d}", ParagraphStyle('FooterTurno', fontSize=18, fontName='Helvetica-Bold', alignment=1, textColor=HexColor('#7f8c8d'))))

    doc.build(elements)
    return buffer.getvalue()
