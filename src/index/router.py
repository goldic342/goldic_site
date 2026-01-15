from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from blog.service import BlogService
from index.utils import last_build


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "description": "Goldic - Fullstack web developer and Linux enthusiast.",
            "title": "Goldic",
        },
    )


@router.get("/favicon.ico")
async def favicon():
    return FileResponse("static/icons/favicon.ico")


@router.get("/robots.txt")
async def robots():
    return FileResponse("static/data/robots.txt")


@router.get("/rss.xml")
async def rss(request: Request):
    time_format = "%a, %d %b %Y %H:%M:%S %z"
    posts = BlogService().get_posts(time_format=time_format)

    return templates.TemplateResponse(
        "xml/rss.xml",
        {
            "request": request,
            "posts": posts,
            "last_build": last_build(posts, time_format),
        },
        media_type="application/rss+xml",
    )


@router.get("/sitemap.xml")
async def sitemap(request: Request):
    time_format = "%Y-%m-%d"
    posts = BlogService().get_posts(time_format=time_format)

    return templates.TemplateResponse(
        "xml/sitemap.xml",
        {
            "request": request,
            "posts": posts,
            "last_build": last_build(posts, time_format),
        },
        media_type="application/rss+xml",
    )
