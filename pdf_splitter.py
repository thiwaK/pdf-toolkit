#!/usr/bin/python

import os
import sys
from PyPDF2 import PdfWriter, PdfReader

try:
    input_pdf_path = sys.argv[1]
    start_page = int(sys.argv[2])
    end_page = int(sys.argv[3])
except Exception as e:
    print('''
    pdf_splitter.py <input pdf> <page start> <page stop>

    ''')
    exit()

output_pdf_name = os.path.splitext(os.path.basename(input_pdf_path))[0] + f"_{start_page}-{end_page}"
output_pdf_path = input_pdf_path.replace(os.path.splitext(os.path.basename(input_pdf_path))[0], output_pdf_name)

pdf_reader = PdfReader(open(input_pdf_path, "rb"))
pdf_writer = PdfWriter()

for page_number in range(start_page, end_page):
    pdf_writer.add_page(pdf_reader.pages[page_number])

with open(output_pdf_path, "wb") as output_file:
    pdf_writer.write(output_file)

