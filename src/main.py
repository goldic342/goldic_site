from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from exceptions import DetailedError
from index.router import router
from blog.router import router as blog_router
from admin.router import router as admin_router
import os
from pathlib import Path
from config import settings

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/up", StaticFiles(directory=settings.DATA_DIR), name="uploads")

os.makedirs(Path(settings.DATA_DIR) / "md", exist_ok=True)
os.makedirs(Path(settings.DATA_DIR) / "media", exist_ok=True)


@app.exception_handler(DetailedError)
async def auth_error_handler(request, exc):
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error": exc.error,
            "detail": exc.detail,
        },
        status_code=403,
    )


app.include_router(router)
app.include_router(blog_router)
app.include_router(admin_router)
