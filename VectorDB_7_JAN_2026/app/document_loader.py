from pypdf import PdfReader
from io import BytesIO

def load_txt(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8")

def load_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)
