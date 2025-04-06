from db.connection import get_connection
from db.schema import create_barriers_table

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
    conn = get_connection()
    create_barriers_table(conn)
    insert_barriers_data(conn, barriers_data, doc_id="doc_001")
    conn.close()
