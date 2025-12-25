import sqlite3
from pathlib import Path

# DBパス
db_path = Path(__file__).parent / "db" / "savelog.sqlite3"

# schema.sqlを読み込む
schema_path = Path(__file__).parent.parent / "schema.sql"

conn = sqlite3.connect(db_path)
with open(schema_path, "r", encoding="utf-8") as f:
    conn.executescript(f.read())

conn.close()

print("SaveLog DB initialized")