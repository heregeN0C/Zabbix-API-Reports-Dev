from fpdf import FPDF
from PIL import Image
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Gráficos', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')


def create_pdf(titles_and_images, output_pdf):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for title, image_path in titles_and_images:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, title, 0, 1, 'C')

        pdf.ln(10)  # Espaçamento antes da imagem

        # Adicionar imagem ao PDF
        try:
            img = Image.open(image_path)
            img_width, img_height = img.size
            aspect_ratio = img_height / img_width
            pdf_width = 190  # Largura máxima permitida no PDF (A4)
            pdf_height = pdf_width * aspect_ratio
            pdf.image(image_path, x=10, y=pdf.get_y(), w=pdf_width, h=pdf_height)
        except FileNotFoundError:
            print(f"Erro: A imagem '{image_path}' não foi encontrada.")

    pdf.output(output_pdf)
    print(f"PDF gerado: {output_pdf}")


# Exemplo de uso

