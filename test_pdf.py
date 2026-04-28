from reportlab.platypus import SimpleDocTemplate, Image
import io, os
buffer = io.BytesIO()
doc = SimpleDocTemplate(buffer)
logo_path = os.path.abspath(os.path.join("assets", "images", "universidad-autonoma-de-coahuila.webp"))
img = Image(logo_path, width=100, height=100)
doc.build([img])
print("PDF built!")
