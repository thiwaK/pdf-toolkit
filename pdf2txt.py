import fitz # install using: pip install PyMuPDF
import concurrent.futures
import os
import sys
import re

multi_threading = 1

class progress():
	def __init__(self, current, maximum):
			self.current = current
			self.maximum = maximum
			self.BAR_WIDTH = 45
			
			self.current -=1
			self.next()
			
	def next(self):
			self.current += 1
			x = int((self.BAR_WIDTH)*self.current/self.maximum)
			y = round(self.current/self.maximum*100, 1)
			text_pb = "{}[{}{}] {}/{} {}%".format("Processing", "#"*x, "."*(self.BAR_WIDTH-x), self.current, self.maximum, y)
			print(text_pb, end='\r', file=sys.stdout, flush=True)

def get_all_pdf(path):
	pdf_paths = []
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith(".pdf"):
				 pdf_paths.append(os.path.join(root, file))
	return pdf_paths

def preprocess(text):
	text = text.replace('\n', ' ')
	text = re.sub('\s+', ' ', text)
	return text

def pdf_to_text(path, start_page=1, end_page=None):
	doc = fitz.open(path)
	total_pages = doc.page_count
	
	if end_page is None:
		end_page = total_pages

	text_list = []

	for i in range(start_page-1, end_page):
		text = doc.load_page(i).get_text("text")
		text = preprocess(text)
		text_list.append(text)

	doc.close()
	text_to_file((text_list, path))

def processed(pdf):
	with open("log.txt", 'a', encoding='utf-8') as f:
		f.write(pdf + "\n")

def text_to_file(item):

	error = 0
	txt = item[0]
	file_name = os.path.splitext(os.path.basename(item[1]))[0]
	root_out_dir = os.path.dirname(item[1])
	

	if len(txt) < 1:
		error = 1
		processed("ERROR: " + item[1])

	out_file = os.path.join(root_out_dir, file_name + ".txt")
	with open(out_file, 'wb') as f:
		for page in txt:
			f.write(page.encode("utf-8") + "\n\n".encode("utf-8"))
	if error == 0:
		processed(item[1])
	p.next()


try:
	pdf_file = sys.argv[1]
except Exception as e:
	print("pdf2text.py [your.pdf] OR [your/path/]")
	exit()

if os.path.isdir(pdf_file):
	print("Lising pdfs...")
	pdf_list = tuple(get_all_pdf(pdf_file))
elif os.path.isfile(pdf_file):
	pdf_list = tuple(pdf_file,)
else:
	print("Check your inputs")
	exit()

print(f"{len(pdf_list)} pdfs found.")

p = progress(0, len(pdf_list))
if multi_threading:
	max_workers = 8
	with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
		results = executor.map(pdf_to_text, pdf_list)
	executor.shutdown()
else:
	for pdf in pdf_list:
		pdf_to_text(pdf)

print("\nDone!")