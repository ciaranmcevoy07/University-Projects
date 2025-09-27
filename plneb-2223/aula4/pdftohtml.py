import pdfkit

pdf_file = open('LIVRO-Doenças-do-Aparelho-Digestivo.pdf', 'rb')
html_file = pdfkit.from_pdf(pdf_file, 'LIVRO-Doenças-do-Aparelho-Digestivo.html')
pdf_file.close()
