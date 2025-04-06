import re
import unicodedata
from concurrent.futures import ProcessPoolExecutor, as_completed

# from wtpsplit import SaT
import syntok.segmenter as segmenter
from tqdm import tqdm

import utils.llm_info_extraction as llm_info_extractor


def clean_text(text):
    text = unicodedata.normalize("NFKC", text)  # Normalize Unicode characters
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"Page \d+ of \d+", "", text)  # Remove page numbers
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Remove non-ASCII characters
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespace
    text = re.sub(r"\n+", "\n", text)  # Remove extra newlines

    return text


def split_text_into_sentences(text):
    sentences = []
    for paragraph in segmenter.analyze(text):
        for sentence in paragraph:
            sentences.append(" ".join(token.value for token in sentence))
    return sentences


def merge_sentences_to_paragraphs(sentences, max_tokens=100, token_count_fn=None):
    paragraphs = []
    current_para = []
    current_tokens = 0

    for sent in sentences:
        tokens = token_count_fn(sent)
        if current_tokens + tokens > max_tokens:
            paragraphs.append(" ".join(current_para))
            current_para = [sent]
            current_tokens = tokens
        else:
            current_para.append(sent)
            current_tokens += tokens

    if current_para:
        paragraphs.append(" ".join(current_para))

    return paragraphs


def rolling_paragraph_chunks(
    paragraphs, source_file=None, window=10, stride=8, token_count_fn=None
):
    chunks = []

    for i in range(0, len(paragraphs) - window + 1, stride):
        chunk_text = " ".join(paragraphs[i : i + window])
        token_count = token_count_fn(chunk_text)

        chunks.append(
            {
                "source_file": source_file,
                "chunk_index": len(chunks),
                "text": chunk_text,
                "token_count": token_count,
                "paragraph_start": i,
                "paragraph_end": i + window - 1,
            }
        )

    return chunks


def split_document_to_chunks(
    text, source_file=None, max_tokens=100, window=10, stride=8
):

    sentences = split_text_into_sentences(text)
    paragraphs = merge_sentences_to_paragraphs(
        sentences, max_tokens=max_tokens, token_count_fn=llm_info_extractor.count_tokens
    )
    chunks = rolling_paragraph_chunks(
        paragraphs,
        source_file=source_file,
        window=window,
        stride=stride,
        token_count_fn=llm_info_extractor.count_tokens,
    )

    return chunks


def split_all_documents_to_chunks(doc_dict, max_workers=4):
    results = {}
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(split_document_to_chunks, text, filename): filename
            for filename, text in doc_dict.items()
        }
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Chunking PDFs"
        ):
            results[futures[future]] = future.result()
    return results
