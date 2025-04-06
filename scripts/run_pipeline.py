from data_cleaning import main as clean_and_chunk
from setup_db import main as setup_db

from utils.db.chunks_queries import insert_chunks
from utils.db.connection import get_db_connection

if __name__ == "__main__":

    chunks_by_file = clean_and_chunk()
    all_chunks_data = [
        chunk_data
        for chunk_list in chunks_by_file.values()
        for chunk_data in chunk_list
    ]
    setup_db()
    conn = get_db_connection()
    insert_chunks(conn, all_chunks_data)
    conn.close()
