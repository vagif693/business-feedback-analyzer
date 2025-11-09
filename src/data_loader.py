import pandas as pd
import pdfplumber
import docx
import pytesseract
from PIL import Image

def load_data(filepath):
    ext = filepath.split('.')[-1].lower()
    try:
        if ext == 'csv':
            df = pd.read_csv(filepath, on_bad_lines='skip')
            return df
        elif ext in ['xls', 'xlsx']:
            df = pd.read_excel(filepath)
            return df
        elif ext == 'txt':
            with open(filepath, 'r') as f:
                text = f.read()
            return pd.DataFrame({'text_response': [text]})
        elif ext == 'pdf':
            text = ''
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + '\n'
            return pd.DataFrame({'text_response': [text]})
        elif ext == 'docx':
            doc = docx.Document(filepath)
            text = "\n".join([para.text for para in doc.paragraphs])
            return pd.DataFrame({'text_response': [text]})
        elif ext in ['png', 'jpeg', 'jpg']:
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img)
            return pd.DataFrame({'text_response': [text]})
        else:
            return pd.DataFrame({'text_response': ["Unsupported file type. Please upload CSV, Excel, TXT, PDF, DOCX, or an image."]})
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame({'text_response': [f"Error loading file: {e}"]})