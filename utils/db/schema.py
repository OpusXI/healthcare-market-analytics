def create_chunks_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            text TEXT NOT NULL,
            token_count INTEGER NOT NULL,
            paragraph_start INTEGER,
            paragraph_end INTEGER,
            processed INTEGER DEFAULT 0
        )
    """
    )
    conn.commit()


def create_chunk_outputs_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chunk_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chunk_id INTEGER NOT NULL,
            llm_output TEXT,
            FOREIGN KEY (chunk_id) REFERENCES chunks(id)
        )
    """
    )
    conn.commit()


def create_barriers_table(conn):
    cursor = conn.cursor()
    # Create table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS barriers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barrier_type TEXT NOT NULL,
            affected_party TEXT NOT NULL,
            description TEXT NOT NULL,
            doc_id TEXT
        )
    """
    )
    conn.commit()
