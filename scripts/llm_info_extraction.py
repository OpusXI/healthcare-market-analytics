import openai

sample_text = """Gene therapy has shown incredible promise in treating rare genetic
disorders, with several recent trials demonstrating positive outcomes. In 2023,
over 50 new therapies were in development globally. However, the cost of treatment
can exceed $2 million, presenting a significant challenge for both private insurers
and national healthcare systems. A recent panel discussion at the Rare Disease
Congress in Berlin emphasized the need for new pricing models. Meanwhile,
advancements in viral vector design are improving delivery efficiency, though rural
hospitals often still lack proper refrigeration equipment. Public perception of gene
editing remains mixed, and some advocacy groups are calling for more transparency
in clinical trial data. In Europe, differences in regulatory approval timelines are
slowing market access in certain countries."""


def get_API_key():
    pass


def get_prompt():
    example_prompt = (
        "I am building an ontology to capture access barriers to gene therapy.\n\n"
        "Can you list the main categories of barriers (e.g., pricing, regulatory, "
        "clinical, ethical), then under each category list the most common or "
        "important subtypes (e.g., for pricing: cost-effectiveness thresholds, payer "
        "reimbursement rules), and for each subtype provide a definition that would "
        "make sense in an ontology?\n\n"
        "Please format the result as:\n"
        "Category:\n"
        "- Subtype: Definition"
    )
    return example_prompt


def send_prompt_to_llm(prompt, model="gpt-4", temperature=0.3, max_tokens=1000):
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
