import pytesseract
from pdf2image import convert_from_path
import os
import fitz

def extract_text_from_pdf(uploaded_file):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        print("PDF Parsing Error:", e)
        return ""