from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import mistune

from blog.service import BlogService

router = APIRouter(prefix="/b")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def list_p(request: Request):
    posts = BlogService().get_posts()

    return templates.TemplateResponse(
        "blog.html",
        {"request": request, "posts": posts},
    )


@router.get("/b")
async def p(request: Request):
    with open("data/md/abc.md", "r") as f:
        d = f.read()

    md = mistune.create_markdown(
        plugins=[
            "strikethrough",
            "footnotes",
            "table",
            "url",
            "task_lists",
            "def_list",
            "abbr",
            "mark",
            "insert",
            "superscript",
            "subscript",
            "math",
            "spoiler",
        ]
    )
    html_content = md(d)

    with open("templates/posts/post.html", "w") as f:
        f.write(str(html_content))

    return FileResponse("templates/posts/post.html", media_type="text/html")
