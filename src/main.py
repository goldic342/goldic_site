from fastapi import FastAPI, HTTPException, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from exceptions import DetailedError
from index.router import router
from blog.router import router as blog_router
from admin.router import router as admin_router
import os
from pathlib import Path
from config import settings

app = FastAPI(
    docs_url=None if settings.IS_PROD else "/docs",
    redoc_url=None if settings.IS_PROD else "/redoc",
    openapi_url=None if settings.IS_PROD else "/openapi.json",
)

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


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": 404,
                "detail": "Page not found",
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error": exc.status_code,
            "detail": exc.detail,
        },
        status_code=exc.status_code,
    )


app.include_router(router)
app.include_router(blog_router)
app.include_router(admin_router)
