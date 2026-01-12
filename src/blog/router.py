from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from pygments.formatters import HtmlFormatter

from datetime import datetime

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


@router.get("/{post_name}")
async def p(post_name: str, request: Request):
    meta, text = BlogService().get_post(post_name)

    if not meta or not text:
        return  # TODO: Not found

    md_text = "".join(text)

    html_content = markdown.markdown(
        md_text,
        extensions=[
            "fenced_code",
            CodeHiliteExtension(linenums=False, guess_lang=True),
            "markdown_sub_sup",
            "markdown_mark",
            "markdown_del_ins",
            "extra",
            "toc",
        ],
    )
    pygments_light_css = HtmlFormatter(style="solarized-light").get_style_defs()
    pygments_dark_css = HtmlFormatter(style="github-dark").get_style_defs()

    return templates.TemplateResponse(
        "post.html",
        {
            "request": request,
            "title": meta.get("name"),
            "content": html_content,
            "pygments_light_css": pygments_light_css,
            "pygments_dark_css": pygments_dark_css,
            "publish_date": datetime.fromtimestamp(
                meta.get("publish_date", 0)
            ).strftime("%B %d %Y"),
        },
    )
