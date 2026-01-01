import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "savelog.sqlite3")

# DB接続用（口座一覧取得）
def get_accounts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM accounts")
    rows = cur.fetchall()


    conn.close()
    return rows

@app.route("/")
def accounts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()


    cur.execute("""
        SELECT a.id, a.name, COALESCE(SUM(s.amount), 0) AS total
        FROM accounts a
        LEFT JOIN savings s
        ON a.id = s.account_id
        GROUP BY a.id, a.name
        ORDER BY a.id
        """)
    accounts = cur.fetchall()

    grand_total = sum(account["total"] for account in accounts)

    conn.close()
    return render_template("index.html", accounts=accounts, grand_total=grand_total)

@app.route("/add", methods=["GET", "POST"])
def add():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    accounts = get_accounts()

    if request.method == "POST":
        account_id = request.form["account_id"]
        amount = request.form["amount"]

        cur.execute(
            "INSERT INTO savings (account_id, amount) VALUES (?, ?)",
            (account_id, amount)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("accounts"))

    conn.close()
    return render_template("add.html", accounts=accounts)

@app.route("/details")
def details():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 確認用
    cur.execute("""PRAGMA table_info(savings)""")
    print(cur.fetchall())

    cur.execute("""
    SELECT s.id, s.amount, s.memo, s.created_at, a.name AS account_name
    FROM savings s
    JOIN accounts a
    ON s.account_id = a.id
    ORDER BY s.created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()

    return render_template("details.html", details=rows)

if __name__ == "__main__":
    # iPhoneからも見られるように
    app.run(host="0.0.0.0", port=5000, debug=True)