import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv


def get_sql_db_path():
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_path)
    return Path(os.getenv("SQL_DB_PATH")).resolve()


def get_db_connection():
    return sqlite3.connect(get_sql_db_path())
