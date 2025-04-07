import json
import time

import pandas as pd
from tqdm import tqdm

from utils.db.connection import get_db_connection
from utils.open_ai_utils import send_messages_to_llm


def get_df_from_db(table_name):
    conn = get_db_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
    conn.close()
    return df


def get_response_from_llm(df, table_name):

    responses = df["response"].tolist()
    for index, row in tqdm(
        df.iterrows(), total=len(df), desc=f"Sending {table_name}_df to LLM"
    ):
        response = send_messages_to_llm(json.loads(row["message"]))
        response_json = response.model_dump()
        responses[index] = json.dumps(response_json)

        if (index + 1) % 3 == 0:
            print("Pausing for 60 seconds to respect rate limits...")
            time.sleep(65)

    df["response"] = responses
    df["status"] = "response received"

    return df


def store_responses_to_db(df, table_name):
    conn = get_db_connection()
    data_to_update = df[["status", "response", "id"]].values.tolist()

    cursor = conn.cursor()
    cursor.executemany(
        f"""
        UPDATE {table_name}
        SET status = ?, response = ?
        WHERE id = ?
        """,
        data_to_update,
    )

    conn.commit()
    conn.close()


def send_one_df_to_llm(table_name):
    df = get_df_from_db(table_name)
    df = get_response_from_llm(df, table_name)
    store_responses_to_db(df, table_name)


def main():

    send_one_df_to_llm("entity_concepts_prompts_and_responses")
    send_one_df_to_llm("relationships_prompts_and_responses")


if __name__ == "__main__":
    main()
