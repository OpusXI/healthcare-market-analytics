import json
import os
from pathlib import Path

import openai
import tiktoken
from dotenv import load_dotenv


def get_API_key():

    load_dotenv()
    key = os.getenv("OPENAI_API_KEY")
    if key is None:
        raise ValueError(
            "API key not found. Please set the " "OPENAI_API_KEY environment variable."
        )
    return key


openai.api_key = get_API_key()


def load_txt_file(file_path):
    """
    Loads a text file and returns its content.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: Content of the text file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_base_prompt():
    base_dir = Path(__file__).parent.resolve().parents[0]
    prompt_path = base_dir / "prompts" / "llm_prompt_v1.txt"
    return load_txt_file(prompt_path)


def get_text_to_analyze():
    base_dir = Path(__file__).parent.resolve().parents[0]
    text_path = base_dir / "sample_text" / "sample_input_text_to_analyze_by_llm_v1.txt"
    return load_txt_file(text_path)


def get_system_prompt():
    base_dir = Path(__file__).parent.resolve().parents[0]
    prompt_path = base_dir / "prompts" / "system_prompt_v1.txt"
    return load_txt_file(prompt_path)


def generate_user_prompt():
    return get_base_prompt().replace("[SAMPLE INPUT TEXT]", get_text_to_analyze())


def create_message(role: str, content: str) -> dict:
    """
    Creates a single message block for OpenAI ChatCompletion.
    Roles: 'system', 'user', or 'assistant'
    """
    return {"role": role, "content": content}


def create_messages(user_prompt: str, system_prompt: str) -> list:
    """
    Builds a list of messages to send to OpenAI API.
    Includes a system prompt (optional) and user prompt.
    """
    return [
        create_message("system", system_prompt),
        create_message("user", user_prompt),
    ]


def get_token_encoder(model: str = "gpt-4o-mini"):
    """
    Returns the token encoder for a given model.
    """
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        print(f"Unknown model '{model}', using default encoding.")
        return tiktoken.get_encoding("cl100k_base")  # Fallback for unknown models


def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """
    Counts the number of tokens in a string for the specified model.
    """
    encoder = get_token_encoder(model)
    return len(encoder.encode(text))


def count_messages_tokens(messages: list, model: str = "gpt-4o-mini") -> int:
    """
    Counts tokens in a list of messages for OpenAI ChatCompletion.
    Pass a tiktoken encoder and the message list.
    """
    # Token rules differ slightly between models
    if "gpt-3.5" in model:
        tokens_per_message = 4
    else:  # gpt-4, gpt-4o, etc.
        tokens_per_message = 3

    total_tokens = 0
    for message in messages:
        total_tokens += tokens_per_message
        for key, value in message.items():
            total_tokens += count_tokens(value, model=model)
    total_tokens += 3  # Priming tokens for reply
    return total_tokens


def load_llm_config():
    """
    Loads the LLM configuration from a JSON file.
    Returns:
        dict: Configuration parameters for the API call.
    """
    base_dir = Path(__file__).parent.resolve().parents[0]
    config_path = base_dir / "config" / "openai_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def send_messages_to_llm(messages, config=None):
    """
    Sends a prompt to the LLM and returns the response.

    Args:
        messages (list): List of messages to send to the LLM.
        config (dict): Configuration parameters for the API call.
            - model (str): Model name (default: "gpt-4o-mini").
            - temperature (float): Sampling temperature (default: 0.7).
            - max_tokens (int): Maximum tokens in the response (default: 1000).
    Returns:
        str: The generated response from the LLM.
    """
    if config is None:
        config = load_llm_config()

    try:
        response = openai.ChatCompletion.create(
            model=config.get("model", "gpt-4o-mini"),
            messages=messages,
            temperature=config.get("temperature", 0),
            max_tokens=config.get("max_tokens", 1000),
        )

        finish_reason = response["choices"][0]["finish_reason"]
        if finish_reason == "length":
            print("Warning: output may have been cut off due to token limit.")

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"


def sandbox():

    user_prompt = generate_user_prompt()
    system_prompt = get_system_prompt()
    messages = create_messages(user_prompt, system_prompt)
    config = load_llm_config()
    response = send_messages_to_llm(messages, config)
    print("LLM Response:")
    print(response)

    return


if __name__ == "__main__":
    sandbox()
