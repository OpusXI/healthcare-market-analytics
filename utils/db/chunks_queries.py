def insert_chunks(conn, chunks: list):
    cursor = conn.cursor()
    try:
        cursor.executemany(
            """
            INSERT INTO chunks (source_file, chunk_index, text, token_count,
                                paragraph_start, paragraph_end)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    chunk["source_file"],
                    chunk["chunk_index"],
                    chunk["text"],
                    chunk["token_count"],
                    chunk.get("paragraph_start"),
                    chunk.get("paragraph_end"),
                )
                for chunk in chunks
            ],
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to insert chunks: {e}")


def get_unprocessed_chunks(conn, limit=None):
    cursor = conn.cursor()

    if limit:
        cursor.execute("""SELECT * FROM chunks WHERE processed = 0 LIMIT ?""", (limit,))
    else:
        cursor.execute("""SELECT * FROM chunks WHERE processed = 0""")
    return cursor.fetchall()


def mark_chunk_processed(conn, chunk_id):
    cursor = conn.cursor()
    cursor.execute("UPDATE chunks SET processed = 1 WHERE id = ?", (chunk_id,))
    conn.commit()
