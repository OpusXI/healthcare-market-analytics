import pandas as pd

from utils.db.chunks_queries import get_unprocessed_chunks
from utils.db.connection import get_db_connection
from utils.prompt_engineer_utils import (
    preapare_messages,
    prepare_system_prompt,
    prepare_user_prompt,
)


def load_db_to_df():
    conn = get_db_connection()
    to_process = get_unprocessed_chunks(conn, limit=None)

    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(chunks)")
    column_names = [info[1] for info in cursor.fetchall()]
    conn.close()

    df = pd.DataFrame(to_process, columns=column_names)
    df.drop(columns=["paragraph_start", "paragraph_end", "processed"], inplace=True)

    return df


def prepare_response(df):
    df["response"] = None
    df["status"] = "staged"
    return df


def load_df_to_db(df):
    conn = get_db_connection()
    df.to_sql("llm_prompts_and_responses", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()


def main():

    system_prompt_file_name = "system_prompt_v1.txt"
    user_prompt_file_name = "entity_concepts_extraction_prompt_v1_ZS_no_examples.txt"

    df = load_db_to_df()
    df = prepare_system_prompt(df, system_prompt_file_name)
    df = prepare_user_prompt(df, user_prompt_file_name)
    df = preapare_messages(df)
    df = prepare_response(df)
    df = load_df_to_db(df)


if __name__ == "__main__":
    main()
