import fitz
from docx import Document
from pathlib import Path


def extract_text(file_path: str) -> str:
    """
    Automatically chooses the correct extractor
    based on the uploaded file type.
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    elif extension == ".docx":
        return extract_docx(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")


def extract_pdf(file_path: str) -> str:
    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_docx(file_path: str) -> str:
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text