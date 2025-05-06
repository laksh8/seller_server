from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.http import FileResponse

def generate_invoice(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Company Info (Header)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Company Name")
    p.setFont("Helvetica", 12)
    p.drawString(100, 735, "Address Line 1, City, State, Zip")
    p.drawString(100, 720, "Phone: (123) 456-7890 | Email: support@company.com")
    p.drawString(100, 705, "Website: www.company.com")
    
    # Invoice Title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(400, 750, "Invoice")

    # Order Info
    p.setFont("Helvetica", 12)
    p.drawString(400, 720, f"Invoice # {order.id}")
    p.drawString(400, 705, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
    p.drawString(400, 690, f"Status: {order.status}")

    # Buyer Info
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 670, f"Buyer: {order.buyer}")

    # Line break for spacing
    p.line(100, 665, 500, 665)

    # Product Table Header
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 640, "Product")
    p.drawString(300, 640, "Quantity")
    p.drawString(400, 640, "Price")
    p.drawString(500, 640, "Total")

    # Product List
    p.setFont("Helvetica", 12)
    y_position = 620
    for item in order.items.all():
        p.drawString(100, y_position, item.product.name)
        p.drawString(300, y_position, str(item.quantity))
        p.drawString(400, y_position, f"${item.price:.2f}")
        p.drawString(500, y_position, f"${item.price * item.quantity:.2f}")
        y_position -= 20

    # Total Amount
    p.setFont("Helvetica-Bold", 14)
    p.drawString(400, y_position - 20, "Total Amount:")
    p.drawString(500, y_position - 20, f"${order.total_amount:.2f}")
    
    # Footer
    p.setFont("Helvetica", 10)
    p.drawString(100, y_position - 40, "Thank you for your business!")
    
    # Save the PDF
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'invoice_order_{order.id}.pdf')
