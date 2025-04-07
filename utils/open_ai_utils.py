import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def get_API_key():
    base_dir = Path(__file__).parent.resolve().parents[0]
    env_path = base_dir / ".env"
    load_dotenv(env_path)
    key = os.getenv("OPENAI_API_KEY")

    if key is None:
        raise ValueError(
            "API key not found. Please set the " "OPENAI_API_KEY environment variable."
        )

    return key


def initialize_openai_client():
    client = OpenAI(api_key=get_API_key())
    return client


def load_openai_config():
    base_dir = Path(__file__).parent.resolve().parents[0]
    config_path = base_dir / "config" / "openai_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def send_messages_to_llm(messages, config=None):
    if config is None:
        config = load_openai_config()

    try:

        client = initialize_openai_client()
        completion = client.chat.completions.create(
            model=config.get("model", "gpt-4o-mini-2024-07-18"),
            messages=messages,
            store=config.get("store", False),
            temperature=config.get("temperature", 0),
            max_completion_tokens=config.get("max_completion_tokens", 1000),
        )

        finish_reason = completion.choices[0].finish_reason
        if finish_reason == "length":
            print("Warning: output may have been cut off due to token limit.")

        return completion

    except Exception as e:
        return f"Error: {e}"
