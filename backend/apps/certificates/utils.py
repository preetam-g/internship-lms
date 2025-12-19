from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors


def generate_certificate_pdf(student_name, course_name, date_str, cert_id):
    """
    Generates a PDF certificate in landscape mode.
    Returns a Django ContentFile ready to be saved to a model.
    """
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # --- Design the Certificate ---

    # Border
    p.setStrokeColor(colors.darkblue)
    p.setLineWidth(5)
    p.rect(30, 30, width - 60, height - 60)

    # Header
    p.setFont("Helvetica-Bold", 36)
    p.drawCentredString(width / 2, height - 100, "Certificate of Completion")

    # Body Text
    p.setFont("Helvetica", 18)
    p.drawCentredString(width / 2, height - 160, "This is to certify that")

    # Student Name
    p.setFont("Helvetica-Bold", 30)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(width / 2, height - 210, student_name)

    # More Body Text
    p.setFont("Helvetica", 18)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, height - 260, "has successfully completed the course")

    # Course Name
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2, height - 300, course_name)

    # Date and ID Footer
    p.setFont("Helvetica", 12)
    p.drawString(50, 50, f"Issued: {date_str}")
    p.drawRightString(width - 50, 50, f"ID: {str(cert_id)}")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf_data = buffer.getvalue()
    buffer.close()

    # Return as a ContentFile with a filename
    filename = f"certificate_{student_name}_{course_name}.pdf".replace(" ", "_")
    return ContentFile(pdf_data, name=filename)