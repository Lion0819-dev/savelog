from fastapi import FastAPI

app = FastAPI(title="SaveLog")


@app.get("/")
def root():
    return {"app": "SaveLog", "status": "ok"}

