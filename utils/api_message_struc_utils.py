import tiktoken


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


def get_token_encoder(model: str = "gpt-4o-mini-2024-07-18"):
    """
    Returns the token encoder for a given model.
    """
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        print(f"Unknown model '{model}', using default encoding.")
        return tiktoken.get_encoding("cl100k_base")  # Fallback for unknown models


def count_tokens(text: str, model: str = "gpt-4o-mini-2024-07-18") -> int:
    """
    Counts the number of tokens in a string for the specified model.
    """
    encoder = get_token_encoder(model)
    return len(encoder.encode(text))


def count_messages_tokens(messages: list, model: str = "gpt-4o-mini-2024-07-18") -> int:
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
