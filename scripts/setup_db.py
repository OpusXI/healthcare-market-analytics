from uitls.db.schema import create_chunks_table

from utils.db.connection import get_connection


def apply_indexes_and_optimizations(conn):
    cursor = conn.cursor()
    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_processed ON chunks(processed);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_source_file ON chunks(source_file);")
    # WAL mode
    cursor.execute("PRAGMA journal_mode=WAL;")
    conn.commit()


if __name__ == "__main__":
    conn = get_connection()
    create_chunks_table(conn)
    apply_indexes_and_optimizations(conn)
    conn.close()
