import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "savelog.sqlite3")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT * FROM savings")

print(cur.fetchall())

cur.execute("""
    UPDATE savings
    SET saved_date = '2025-11-01 10:00'
    WHERE id = 12
""")

print("更新件数:", cur.rowcount)

conn.commit()
conn.close()
