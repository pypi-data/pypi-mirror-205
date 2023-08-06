from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def generate_recipe_pdf(recipe):
    # Set up the PDF canvas
    c = canvas.Canvas("recipe.pdf", pagesize=letter)

    # Set up the stylesheet for the recipe text
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleH = styles["Heading1"]

    # Add the recipe title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(1 * inch, 10.5 * inch, recipe.title)
    c.line(1 * inch, 10.45 * inch, 7.5 * inch, 10.45 * inch)

    # Add the ingredients
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, 9.5 * inch, "Ingredients:")
    c.setFont("Helvetica", 12)
    i = 0
    for ingredient in recipe.ingredients:
        c.drawString(1.5 * inch, (9.5 - i) * inch, "- " + ingredient)
        i += 0.2

    # Add the directions
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, 7 * inch, "Directions:")
    c.setFont("Helvetica", 12)
    i = 0
    for direction in recipe.directions:
        c.drawString(1.5 * inch, (7 - i) * inch, "- " + direction)
        i += 0.2

    # Save the PDF document
    c.save()

    # Return the PDF document
    with open("recipe.pdf", "rb") as f:
        pdf = f.read()
    return pdf
