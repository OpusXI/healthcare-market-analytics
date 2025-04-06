import utils.data_cleaning as data_cleaner


def main():
    texts = data_cleaner.extract_text_from_pdfs(data_cleaner.get_raw_data_path())
    return texts


if __name__ == "__main__":
    main()
