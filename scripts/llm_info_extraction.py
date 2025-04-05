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

sample_output = [
    {
        "barrier_type": "cost",
        "affected_party": "payer",
        "description": "The cost of treatment can exceed $2 million, presenting a "
        "significant challenge for both private insurers and national healthcare "
        "systems.",
    },
    {
        "barrier_type": "infrastructure",
        "affected_party": "provider",
        "description": "Rural hospitals often still lack proper refrigeration "
        "equipment.",
    },
    {
        "barrier_type": "regulatory",
        "affected_party": "policymaker",
        "description": "Differences in regulatory approval timelines are slowing "
        "market access in certain countries.",
    },
]

"""NOISE: Rare Disease Congress in Berlin, viral vector design, public perception
transparency in trial data, 50 new therapies"""


def get_API_key():
    pass


def get_prompt():
    example_prompt = (
        "I am building a custom ontology to classify access barriers to gene "
        "therapy.\n\nBelow is some unstructured text. Please read it carefully and "
        "extract the major access barriers.\n\nFor each barrier you identify, output a "
        "JSON object with the following keys:\n - barrier_type: the general type of "
        "access issue (e.g., cost, regulatory, infrastructure)\n- affected_party: "
        "who is impacted the most by this barrier (e.g., patient, provider, payer, "
        "policymaker)\n- description: a short summary of the issue in natural "
        "language\n\nPlease return the result as a Python list of dictionaries. \n\n"
        "Now analyze the following text and extract the relevant access barriers:\n"
    )

    return example_prompt


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
