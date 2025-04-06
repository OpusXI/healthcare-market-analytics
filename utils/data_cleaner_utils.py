import re
import textwrap
import unicodedata


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
