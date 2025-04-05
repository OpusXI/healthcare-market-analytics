import os
import textwrap
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pdfplumber
from dotenv import load_dotenv


def get_raw_data_path():
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)
    pdf_folder_path = os.getenv("RAW_DATA_PATH")

    return pdf_folder_path


def extract_text_from_single_pdf(pdf_folder_path, filename):
    pdf_path = os.path.join(pdf_folder_path, filename)
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(
            page.extract_text() for page in pdf.pages if page.extract_text()
        )

    return text


def extract_text_from_pdfs(pdf_folder_path, max_workers=4):
    all_docs = {}
    filenames = [f for f in os.listdir(pdf_folder_path) if f.endswith(".pdf")]

    # SAND BOXING  REMEMBER TO DELTE #
    filenames = filenames[2:]
    # SAND BOXING  REMEMBER TO DELTE #

    # Create a ThreadPoolExecutor to handle multiple PDF files concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks to the executor for each PDF file
        # and store the future objects in a dictionary
        future_to_file = {
            executor.submit(extract_text_from_single_pdf, pdf_folder_path, f): f
            for f in filenames
        }

        # Iterate over the completed futures as they finish
        # reducing dead time
        for future in as_completed(future_to_file):
            filename = future_to_file[future]
            try:
                all_docs[filename] = future.result()
                print(f"Extracted: {filename}")
            except Exception as e:
                print(f"Failed on {filename}: {e}")

    return all_docs


def chunk_text(text, chunk_size):
    return textwrap.wrap(text, chunk_size)


def chunk_texts(all_docs, chunk_size=300):
    chunked_docs = {}
    for filename, text in all_docs.items():
        # cleaned_text = clean_text(text)
        chunked_docs[filename] = chunk_text(text, chunk_size)
    return chunked_docs


def sandbox():
    pdf_folder_path = get_raw_data_path()
    all_docs = extract_text_from_pdfs(pdf_folder_path)
    chunked_docs = chunk_texts(all_docs, chunk_size=300)

    return chunked_docs


if __name__ == "__main__":
    sandbox()
