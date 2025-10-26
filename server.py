from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"BGDB Cloud": "FastAPI server is running successfully!"}
