from pathlib import Path


def get_base_dir():
    return Path(__file__).parent.resolve().parents[0]


def load_txt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_system_prompt(system_prompt_file_name):
    base_dir = get_base_dir()
    prompt_path = base_dir / "prompts" / system_prompt_file_name
    return load_txt_file(prompt_path)


def get_base_prompt(base_prompt_file_name):
    base_dir = get_base_dir()
    prompt_path = base_dir / "prompts" / base_prompt_file_name
    return load_txt_file(prompt_path)


def get_text_to_analyze(text_file_name):
    base_dir = get_base_dir()
    text_path = base_dir / "sample_text" / text_file_name
    return load_txt_file(text_path)


def generate_user_prompt(base_prompt_file_name, text_file_name):
    return get_base_prompt(base_prompt_file_name).replace(
        "[INSERT CHUNK]", get_text_to_analyze(text_file_name)
    )
