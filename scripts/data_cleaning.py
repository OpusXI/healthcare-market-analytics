import os
import textwrap
from pathlib import Path

import pdfplumber
from dotenv import load_dotenv


def get_raw_data_path():
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)
    pdf_folder_path = os.getenv("RAW_DATA_PATH")

    return pdf_folder_path


def extract_text_from_pdfs(pdf_folder_path):
    all_docs = {}
    for filename in os.listdir(pdf_folder_path):
        if filename.endswith(".pdf"):
            with pdfplumber.open(os.path.join(pdf_folder_path, filename)) as pdf:
                text = "\n".join(
                    page.extract_text() for page in pdf.pages if page.extract_text()
                )
                all_docs[filename] = text
    return all_docs


def chunk_text(text, chunk_size=300):
    return textwrap.wrap(text, chunk_size)


def sandbox():
    pdf_folder_path = get_raw_data_path()
    all_docs = extract_text_from_pdfs(pdf_folder_path)
    return all_docs
    """for filename, text in all_docs.items():
        print(f"Processing {filename}...")
        chunks = chunk_text(text)
        print(f"Number of chunks: {len(chunks)}")
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}: {chunk}\n")"""


if __name__ == "__main__":
    sandbox()
