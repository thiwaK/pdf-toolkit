import os
import sys
import PyPDF2

if len(sys.argv) !=2:
	
	print(r"""
	pdf unlocker 0.1
	-----------------

	Usage:
		unlock_pdf.py name.pdf""")
	exit()

input_pdf = sys.argv[1]
output_pdf = os.path.splitext(input_pdf)[0] + "_unlock.pdf"

pdf_writer = PyPDF2.PdfWriter()
pdf_reader = PyPDF2.PdfReader(input_pdf)
page_count = len(pdf_reader.pages)

for i in range(0, page_count):
	page_obj = pdf_reader.pages[i]
	pdf_writer.add_page(page_obj)

pdf_out = open(output_pdf, 'wb')
pdf_writer.write(pdf_out)
pdf_out.close()
