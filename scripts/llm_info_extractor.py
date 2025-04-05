import utils.prompt_engineer_utils as prompt_engineer


def main():
    sys_prompt = prompt_engineer.get_system_prompt("system_prompt_v1.txt")
    user_prompt = prompt_engineer.generate_user_prompt(
        "entity_concepts_extraction_prompt_v1_ZS_no_examples.txt",
        "sample_input_text_to_analyze_by_llm_v1.txt",
    )

    print(f"System Prompt: {sys_prompt}")
    print(f"User Prompt: {user_prompt}")


if __name__ == "__main__":
    main()
