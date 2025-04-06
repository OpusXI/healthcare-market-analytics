from utils.db.connection import get_db_connection
from utils.db.schema import (
    create_chunks_table,
    create_entity_concepts_extraction_prompts_and_responses_table,
)


def apply_indexes_and_optimizations(conn):
    cursor = conn.cursor()
    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_processed ON chunks(processed);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_source_file ON chunks(source_file);")
    # WAL mode
    cursor.execute("PRAGMA journal_mode=WAL;")
    conn.commit()


def main():
    conn = get_db_connection()
    create_chunks_table(conn)
    create_entity_concepts_extraction_prompts_and_responses_table(conn)
    apply_indexes_and_optimizations(conn)
    conn.close()


if __name__ == "__main__":
    main()
