import csv
import os
from collections import defaultdict
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import PCMYKColor

# Datas configuration and loading
csv_folder = 'csv'
books_data = defaultdict(list)

# Load data from csv files
for csv_file in os.listdir(csv_folder):
    if csv_file.endswith('.csv'):
        category = csv_file.replace('.csv', '')
        with open(os.path.join(csv_folder, csv_file), newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                books_data[category].append(row)

# Graphics functions

def pie_chart(c, data, x_pos, y_pos):
    """
    Create a pie chart illustrating the distribution of books per category.

    Args:
        c (canvas.Canvas): Canvas
        data (dict): Data to display
        x_pos (int): x-coordinate for positioning
        y_pos (int): y-coordinate for positioning
    
    Returns:
        None
    """
    drawing = Drawing(200, 200)
    pie = Pie()
    pie.x = 50
    pie.y = 0
    pie.width = 200
    pie.height = 200
    pie.data = list(data.values())
    pie.labels = list(data.keys())
    drawing.add(pie)
    drawing.drawOn(c, x_pos, y_pos)

def bar_chart(c, data, x_pos, y_pos):
    """
    Create a bar chart illustrating the average price of books per category.

    Args:
        c (canvas.Canvas): Canvas
        data (dict): Data to display
        x_pos (int): X position to draw the chart
        y_pos (int): Y position to draw the chart
    
    Returns:
        None
    """
    drawing = Drawing(400, 200)
    bar = VerticalBarChart()
    bar.x = 50
    bar.y = 50
    bar.height = 200
    bar.width = 300
    bar.data = [list(data.values())]
    bar.categoryAxis.categoryNames = list(data.keys())
    bar.categoryAxis.labels.angle = 90
    bar.categoryAxis.labels.dx = -8  
    bar.categoryAxis.labels.dy = -30
    bar.valueAxis.valueMin = 0
    bar.valueAxis.valueMax = max(data.values()) + 10
    bar.bars[0].fillColor = PCMYKColor(0, 100, 100, 40, alpha=85)
    drawing.add(bar)
    drawing.drawOn(c, x_pos, y_pos)

#Simplifie calculate stats

# Calculate stats
category_distribution = {category: len(books) for category, books in books_data.items()}
category_avg_price = {}

for category, books in books_data.items():
    total_price = sum(float(book['price_including_tax'].replace('£', '')) for book in books)
    avg_price = total_price / len(books)
    category_avg_price[category] = avg_price

# Key statistics
overall_avg_price = sum(category_avg_price.values()) / len(category_avg_price)
most_represented_category = max(category_distribution, key=category_distribution.get)
highest_avg_price_category = max(category_avg_price, key=category_avg_price.get)

# Fonction de création du PDF
def create_pdf():
    """
    Create a PDF report with improved layout, positioning each chart 20px below its title.

    Args:
        None

    Returns:
        None
    """

    c = canvas.Canvas("rapport_prix_livres.pdf", pagesize=letter)
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 750, "Rapport des prix des livres d'occasion")
    
    # Subtitle
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, "Analyse des prix des livres d'occasion par catégorie")

    # Pie Chart Section - Répartition des livres par catégorie
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 700, "Répartition des livres par catégorie")
    c.setFont("Helvetica", 12)
    c.drawString(100, 680, "Ce diagramme circulaire montre la répartition des livres par catégorie.")
    
    pie_chart(c, category_distribution, x_pos=100, y_pos=445)

    # Bar Chart Section - Prix moyen des livres par catégorie
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 410, "Prix moyen des livres par catégorie")
    c.setFont("Helvetica", 12)
    c.drawString(100, 390, "Ce graphique en barres montre le prix moyen des livres pour chaque catégorie.")
    
    bar_chart(c, category_avg_price, x_pos=100, y_pos=130)

    # Key Statistics Section - Statistiques clés
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 100, "Statistiques clés")
    c.setFont("Helvetica", 12)
    c.drawString(100, 80, f"Prix moyen global des livres : £{overall_avg_price:.2f}")
    c.drawString(100, 60, f"Catégorie la plus représentée : {most_represented_category}")
    c.drawString(100, 40, f"Catégorie avec le prix moyen le plus élevé : {highest_avg_price_category}")

    # Save PDF
    c.showPage()
    c.save()

create_pdf()
