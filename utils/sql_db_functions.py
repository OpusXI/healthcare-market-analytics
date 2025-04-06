import sqlite3

from db.connection import get_sql_db_path

# Sample data from your JSON
barriers_data = [
    {
        "barrier_type": "cost",
        "affected_party": "payer",
        "description": "The high cost of gene therapy makes it "
        "unaffordable for most insurers.",
    },
    {
        "barrier_type": "infrastructure",
        "affected_party": "provider",
        "description": "Rural hospitals lack the facilities to store"
        " and administer gene therapies.",
    },
]


def init_sql_db():

    sql_db_path = get_sql_db_path()
    conn = sqlite3.connect(sql_db_path)
    return conn


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


def insert_barriers_data(conn, barriers, doc_id=None):
    cursor = conn.cursor()
    try:
        for barrier in barriers:
            cursor.execute(
                """
                INSERT INTO barriers (barrier_type, affected_party, description, doc_id)
                VALUES (?, ?, ?, ?)
            """,
                (
                    barrier.get("barrier_type"),
                    barrier.get("affected_party"),
                    barrier.get("description"),
                    doc_id,
                ),
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to insert barriers (rolled back): {e}")


def update_barrier_description(conn, barrier_id, new_description):
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE barriers SET description = ? WHERE id = ?
    """,
        (new_description, barrier_id),
    )
    conn.commit()


def delete_barrier_by_id(conn, barrier_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM barriers WHERE id = ?", (barrier_id,))
    conn.commit()


def query_data(conn, query, params=(), fetch_one=False):
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchone() if fetch_one else cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")
        return None


if __name__ == "__main__":
    conn = init_sql_db()
    create_barriers_table(conn)
    insert_barriers_data(conn, barriers_data, doc_id="doc_001")
    conn.close()
