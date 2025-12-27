import sqlite3
from pathlib import Path

conn = sqlite3.connect("savelog.db")
cur = conn.cursor()

# ==== テーブル作成 ====
cur.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# ==== 初期データ投入 ====
accounts = ["Main Bank", "Cash"]

for name in accounts:
    cur.execute(
        "INSERT INTO accounts (name) VALUES (?)",
        (name,)
    )


conn.commit()
conn.close()

print("DB初期化完了")