import sqlite3
from pathlib import Path

conn = sqlite3.connect("savelog.db")
cur = conn.cursor()

# ==== テーブル作成 ====
cur.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS savings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    memo TEXT,
    FOREIGN KEY(account_id) REFERENCES accounts(id)
);
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