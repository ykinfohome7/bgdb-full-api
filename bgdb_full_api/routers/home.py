
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["home"])

@router.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head><title>BGDB Cloud</title></head>
    <body>
        <h1>BGDB Cloud Public API</h1>
        <ul>
            <li><a href="/docs">Swagger UI</a></li>
            <li><a href="/health">Health</a></li>
            <li><a href="/users">Users</a></li>
        </ul>
    </body>
    </html>
    """
