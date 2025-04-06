import utils.data_cleaner_utils as data_cleaner
import utils.pdf_extractor_utils as pdf_extractor


def main():
    texts_dict = pdf_extractor.extract_text_from_pdfs(pdf_extractor.get_raw_data_path())
    chunks_dict = data_cleaner.split_all_documents_to_chunks(texts_dict)
    return chunks_dict


if __name__ == "__main__":
    main()
