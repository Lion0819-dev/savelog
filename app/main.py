import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

DB_PATH = "savelog.db"

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
    accounts = get_accounts()
    return render_template("index.html", accounts=accounts)

@app.route("/add")
def add():
    return render_template("add.html")

if __name__ == "__main__":
    # iPhoneからも見られるように
    app.run(host="0.0.0.0", port=5000, debug=True)