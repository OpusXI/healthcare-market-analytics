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


def create_entity_concepts_prompts_and_responses_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS entity_concepts_prompts_and_responses (
            id INTEGER PRIMARY KEY,
            source_file TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            text TEXT NOT NULL,
            token_count INTEGER NOT NULL,
            system_prompt_ver TEXT,
            system_prompt TEXT,
            user_prompt_ver TEXT,
            user_prompt TEXT,
            message TEXT,           -- JSON string (list of message dicts)
            response TEXT,           -- Raw model response (optional at start)
            status TEXT DEFAULT 'staged'
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
