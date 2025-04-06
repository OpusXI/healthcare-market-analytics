import json
from pathlib import Path

from utils.api_message_struc_utils import create_messages


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


def generate_user_prompt(base_prompt_file_name, text):
    return get_base_prompt(base_prompt_file_name).replace("[INSERT CHUNK]", text)


def prepare_system_prompt(df, system_prompt_file_name):
    df["system_prompt_ver"] = system_prompt_file_name
    df["system_prompt"] = df["system_prompt_ver"].apply(get_system_prompt)
    return df


def prepare_user_prompt(df, user_prompt_file_name):
    df["user_prompt_ver"] = user_prompt_file_name
    df["user_prompt"] = df.apply(
        lambda x: generate_user_prompt(x["user_prompt_ver"], x["text"]), axis=1
    )
    return df


def preapare_messages(df):
    df["message"] = df.apply(
        lambda x: create_messages(x["user_prompt"], x["system_prompt"]), axis=1
    )
    df["message"] = df["message"].apply(json.dumps)
    return df
