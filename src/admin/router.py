from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Query,
    Request,
    UploadFile,
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import quote_plus

from admin.dependencies import verify_token
from admin.service import AdminService
from admin.utils import rate_limit, url_to_meta

router = APIRouter(prefix="/a")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def admin(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", dependencies=[Depends(rate_limit)])
async def admin_login(
    username: str = Form(...),
    password: str = Form(...),
):
    token = AdminService().login(username, password)

    response = RedirectResponse(
        "/a/dash",
        status_code=302,
    )

    response.set_cookie(
        key="toooken",
        value=token,
        secure=True,
        httponly=True,
        path="/",
        samesite="strict",
    )

    return response


@router.get("/dash", dependencies=[Depends(verify_token)])
async def admin_dash(
    request: Request,
    imgs: list[str] | None = Query(None),
    md: str | None = Query(None),
):

    imgs_proc = [url_to_meta(u) for u in imgs] if imgs else None
    md_proc = url_to_meta(md) if md else None

    return templates.TemplateResponse(
        "dash.html",
        {
            "request": request,
            "imgs": imgs_proc or [],
            "md": md_proc,
        },
    )


@router.post("/upimgs", dependencies=[Depends(verify_token)])
async def handle_upload_img(files: list[UploadFile] = File(...)):

    urls = await AdminService().save_files(files, "img")
    redirect_url = "/a/dash?imgs=" + "&imgs=".join(quote_plus(url) for url in urls)

    response = RedirectResponse(redirect_url, status_code=302)

    return response


@router.post("/upmd", dependencies=[Depends(verify_token)])
async def handle_upload_md(file: UploadFile = File(...)):

    urls = await AdminService().save_files([file], "md")
    response = RedirectResponse(f"/a/dash?md={quote_plus(urls[0])}", status_code=302)
    return response
