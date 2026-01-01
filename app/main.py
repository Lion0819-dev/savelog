import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "savelog.sqlite3")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def accounts():
    """
    口座管理画面
    ・口座一覧
    ・各口座の残高
    ・全口座の合計
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            a.id,
            a.name,
            COALESCE(SUM(s.amount), 0) AS balance
        FROM accounts a
        LEFT JOIN savings s ON a.id = s.account_id
        GROUP BY a.id, a.name
        ORDER BY a.id
    """)
    rows = cur.fetchall()
    conn.close()

    # 表示用データ整形（カンマ付き）
    accounts = []
    for r in rows:
        accounts.append({
            "id": r["id"],
            "name": r["name"],
            "balance": r["balance"],
            "balance_str": f"{r['balance']:,}"
        })

    total_amount = sum(r["balance"] for r in rows)
    total_amount_str = f"{total_amount:,}"

    return render_template(
        "index.html",
        accounts=accounts,
        total_amount_str=total_amount_str
    )


@app.route("/add_account", methods=["POST"])
def add_account():
    """
    口座追加
    """
    name = request.form["name"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO accounts (name) VALUES (?)",
        (name,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("accounts"))


@app.route("/delete_account/<int:account_id>", methods=["POST"])
def delete_account(account_id):
    """
    残高0の口座のみ削除
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # 残高チェック
    cur.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM savings
        WHERE account_id = ?
    """, (account_id,))
    balance = cur.fetchone()[0]

    if balance == 0:
        cur.execute(
            "DELETE FROM accounts WHERE id = ?",
            (account_id,)
        )
        conn.commit()

    conn.close()
    return redirect(url_for("accounts"))


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    貯金追加画面
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM accounts")
    accounts = cur.fetchall()

    if request.method == "POST":
        account_id = request.form["account"]
        amount = request.form["amount"]
        memo = request.form.get("memo", "")

        cur.execute("""
            INSERT INTO savings (account_id, amount, memo, saved_date)
            VALUES (?, ?, ?, DATE('now'))
        """, (account_id, amount, memo))

        conn.commit()
        conn.close()
        return redirect(url_for("accounts"))

    conn.close()
    return render_template("add.html", accounts=accounts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
