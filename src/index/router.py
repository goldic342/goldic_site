from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from blog.service import BlogService


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/favicon.ico")
async def favicon():
    return FileResponse("static/icons/favicon.ico")


@router.get("/robots.txt")
async def robots():
    return FileResponse("static/data/robots.txt")


@router.get("/rss.xml")
async def rss(request: Request):
    posts = BlogService().get_posts(time_format="%a, %d %b %Y %H:%M:%S %z")

    return templates.TemplateResponse(
        "rss.xml",
        {
            "request": request,
            "posts": posts,
            "last_build": posts[0].get("publish_date"),
        },
        media_type="application/rss+xml",
    )
