import pymupdf
import re
import os
import locale
import tempfile
from pypdf import PdfReader, PdfWriter

def merge_pdfs(pdf_files):
    merge_writer = PdfWriter()

    # Use the provided list of file paths directly instead of scanning a folder
    for filepath in pdf_files:
        reader = PdfReader(filepath)
        for page in reader.pages:
            merge_writer.add_page(page)

    # Create a temporary file for the merged PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix="_merged.pdf") as temp_file:
        temp_path = temp_file.name
        merge_writer.write(temp_file)
    
    # Return the path to the temporary merged file
    return temp_path

def find_name(text):
    try: 
        beginning = text.find("\nSoyadı\xa0/\xa0Ünvanı\n:\n")
        end = text.find("\nAdı\n:\n")
        
        return text[beginning + 19:end]
    except:
        return "Null"

def page_traverse(pdf_path):
    global pages
    global_page_number = 0
    doc = pymupdf.open(pdf_path)
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

def sort_pages(pages):
    return sorted(pages, key=lambda p: locale.strxfrm(p['receiver']))

 
def sort_and_save(merged_pdf_path, output_path):
    sorted_pages = sort_pages(pages)
    page_order = []

    for page in sorted_pages:
        page_order.append(page['page_number'])

    reader = PdfReader(merged_pdf_path)
    writer = PdfWriter()

    for i in page_order:
        writer.add_page(reader.pages[i])
        
    with open(output_path, "wb") as f:
        writer.write(f)


def main(pdf_files, output_path):
    locale.setlocale(locale.LC_COLLATE, 'tr_TR.UTF-8')
    
    # Merge the input PDFs into a temporary merged file
    merged_pdf_path = merge_pdfs(pdf_files)
    
    # Process the merged PDF
    page_traverse(merged_pdf_path)
    
    # Sort the pages and save to the output path
    sort_and_save(merged_pdf_path, output_path)
    
    # Clean up the temporary merged PDF file
    try:
        os.unlink(merged_pdf_path)
    except Exception as e:
        print(f"Could not delete temporary merged file {merged_pdf_path}: {e}")
    
    return output_path

