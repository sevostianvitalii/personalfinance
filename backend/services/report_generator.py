from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

class ReportGenerator:
    def generate_report(self, data, filename="report.pdf"):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        elements.append(Paragraph("Financial Report", styles['Title']))
        elements.append(Spacer(1, 12))
        
        # Data is a list of dicts: date, income, expenses, net
        if not data:
            elements.append(Paragraph("No data available for this period.", styles['Normal']))
        else:
            table_data = [["Date", "Income", "Expenses", "Net"]]
            for row in data:
                table_data.append([
                    row['date'], 
                    f"{row['income']:.2f}", 
                    f"{row['expenses']:.2f}", 
                    f"{row['net']:.2f}"
                ])
                
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
            
        doc.build(elements)
        return filename
