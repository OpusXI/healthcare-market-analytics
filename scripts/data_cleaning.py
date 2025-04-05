import os
import re
import textwrap
import unicodedata
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
            page.extract_text(x_tolerance=1, y_tolerance=1)
            for page in pdf.pages
            if page.extract_text()
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


def clean_text(text):
    text = unicodedata.normalize("NFKC", text)  # Normalize Unicode characters
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"Page \d+ of \d+", "", text)  # Remove page numbers
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Remove non-ASCII characters
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespace
    text = re.sub(r"\n+", "\n", text)  # Remove extra newlines

    return text


def chunk_text(text, chunk_size):
    return textwrap.wrap(text, chunk_size)


def chunk_texts(all_docs, chunk_size=300):
    chunked_docs = {}
    for filename, text in all_docs.items():
        cleaned_text = clean_text(text)
        chunked_docs[filename] = chunk_text(cleaned_text, chunk_size)
    return chunked_docs


def sandbox():
    pdf_folder_path = get_raw_data_path()
    all_docs = extract_text_from_pdfs(pdf_folder_path)
    chunked_docs = chunk_texts(all_docs, chunk_size=300)

    for filename, chunks in chunked_docs.items():
        print(f"Chunks for {filename}:")
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i + 1}: {chunk}")
        print("\n")

    return chunked_docs


if __name__ == "__main__":
    sandbox()
