from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI(title="SaveLog")

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/add", response_class=HTMLResponse)
def add_form(request: Request):
    accounts = get_accounts()
    
    return templates.TemplateResponse(
        "add.html",
        {
            "request": request,
            "accounts": accounts            
        }
    )

def get_accounts():
    conn = sqlite3.connect("savelog.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM accounts ORDER BY id")
    acocunts = cur.fetchall()

    conn.close()
    return acocunts