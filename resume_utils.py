import re
import pdfplumber
import docx2txt

def clean_resume(txt):
    txt = re.sub('http\\S+\\s',' ',txt)
    txt = re.sub('@\\S+',' ',txt)
    txt = re.sub('#\\S+\\s',' ',txt)
    txt = re.sub('\\s+',' ',txt)
    return txt

def extract_text(path):
    if path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif path.endswith(".docx"):
        return docx2txt.process(path)

    return ""