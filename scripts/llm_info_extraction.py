from pathlib import Path

import openai


def get_API_key():
    pass


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


def generate_prompt():
    return get_base_prompt().replace("[SAMPLE INPUT TEXT]", get_text_to_analyze())


def send_prompt_to_llm(prompt, model="gpt-4", temperature=0, max_tokens=1000):
    """
    Sends a prompt to the LLM and returns the response.

    Args:
        prompt (str): The input text prompt to send to the LLM.
        model (str): The model to use (e.g., 'gpt-4', 'gpt-3.5-turbo').
        temperature (float): Sampling temperature.
        max_tokens (int): Max number of tokens in the response.

    Returns:
        str: The generated response from the LLM.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a biomedical ontology expert."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"


def sandbox():
    print(generate_prompt())
    return


if __name__ == "__main__":
    sandbox()
