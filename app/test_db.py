import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "db" / "savelog.sqlite3"
conn = sqlite3.connect(db_path)

cur = conn.cursor()

# 貯金を1件追加
cur.execute("""
INSERT INTO savings (account_id, amount, saved_date, memo)
VALUES (?, ?, ?, ?)
""", (1, 10000, "2025-01-10", "初回貯金"))

conn.commit()

# 確認
cur.execute("""
SELECT a.name, s.amount, s.saved_date, s.memo
FROM savings s
JOIN accounts a ON a.id = s.account_id
""")

for row in cur.fetchall():
    print(row)

conn.close()
print("insert savings done")