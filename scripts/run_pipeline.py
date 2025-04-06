from data_cleaning import main as clean_and_chunk
from setup_db import main as setup_db

from utils.db.chunk_queries import get_to_process, insert_chunks
from utils.db.connection import get_db_connection

if __name__ == "__main__":

    chunks = clean_and_chunk()
    setup_db()

    conn = get_db_connection()
    insert_chunks(conn, chunks)
    to_process = get_to_process(conn, limit=10)
