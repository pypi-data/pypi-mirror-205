from bookstore.models import Book
from django.http import HttpResponse
from reportlab.pdfgen import canvas


def count_books():
    return Book.objects.all().count()





def generate_pdf(file_name):
    # Create a new PDF document
    pdf = canvas.Canvas(file_name)

    # Add some text to the PDF
    pdf.drawString(100, 750, "Welcome to Generate PDF package")

    # Save the PDF
    pdf.save()


