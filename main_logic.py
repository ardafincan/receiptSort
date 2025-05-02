# %%
import fitz  
import re
import os
import locale
from pypdf import PdfMerger, PdfReader, PdfWriter

# %%
merger = PdfMerger()

pdf_folder = "./input_pdfs"

pdf_files = sorted(f for f in os.listdir(pdf_folder) if f.endswith(".pdf"))

for filename in pdf_files:
    filepath = os.path.join(pdf_folder, filename)
    merger.append(filepath)

with open("merged_receipts.pdf", "wb") as f:
    merger.write(f)

# %%
def find_name(text):
    try: 
        beginning = text.find("\nSoyadı\xa0/\xa0Ünvanı\n:\n")
        end = text.find("\nAdı\n:\n")
        
        return text[beginning + 19:end]
    except:
        return "Null"

# %%
global_page_number = 0
doc = fitz.open("merged_receipts.pdf")
pages = []
for page in doc:
    
    receiver_name = find_name(page.get_text())
    page = {
       "page_number": global_page_number,
       "page_text": page.get_text("text"),
       "receiver": receiver_name
    }
    pages.append(page)
    global_page_number += 1

# %%
locale.setlocale(locale.LC_COLLATE, 'tr_TR.UTF-8')

def sort_pages(pages):
    return sorted(pages, key=lambda p: locale.strxfrm(p['receiver']))

# %%
sorted_pages = sort_pages(pages)
page_order = []

for page in sorted_pages:
    page_order.append(page['page_number'])

reader = PdfReader("merged_receipts.pdf")
writer = PdfWriter()

for i in page_order:
    writer.add_page(reader.pages[i])
    
with open("reordered_output.pdf", "wb") as f:
    writer.write(f)


