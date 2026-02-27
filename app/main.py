from fastapi import FastAPI
from app.api.routes import router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Decision Companion System")

app.include_router(router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/ui")
def serve_ui():
    return FileResponse("app/static/index.html")