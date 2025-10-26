
from fastapi import FastAPI
app = FastAPI(title="BGDB Dev API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "BGDB Dev API is running"}
