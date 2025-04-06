import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pdfplumber
from dotenv import load_dotenv


def get_raw_data_path():
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)
    pdf_folder_path = os.getenv("RAW_DATA_PATH")

    return pdf_folder_path


def check_spacing_in_extracted_text(filename, text):
    """A function to check if the extracted text is glued together.
    This is a heuristic check based on the ratio of words to characters.
    If the ratio is too low, it may indicate that the text is not properly spaced.
    And there is a need to lower the tolerance in pdfplumber.
    """
    word_count = len(text.split())
    char_count = len(text)

    if char_count > 0 and word_count / char_count < 0.10:  # Low word density
        print(
            f"Warning: Suspicious word spacing in {filename} "
            f"(words/char: {word_count}/{char_count})"
        )

    return text


def extract_text_from_single_pdf(pdf_folder_path, filename):
    pdf_path = os.path.join(pdf_folder_path, filename)
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(
            page.extract_text(x_tolerance=1, y_tolerance=1)
            for page in pdf.pages
            if page.extract_text()
        )

    # Check for spacing issues in the extracted text
    text = check_spacing_in_extracted_text(filename, text)

    return text


def extract_text_from_pdfs(pdf_folder_path, max_workers=4):
    all_docs = {}
    filenames = [f for f in os.listdir(pdf_folder_path) if f.endswith(".pdf")]

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
