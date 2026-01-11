from json import decoder
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Query,
    Request,
    UploadFile,
)
import os
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import urlparse, quote_plus

from admin.dependencies import verify_token
from admin.service import AdminService

router = APIRouter(prefix="/a")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def admin(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
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


@router.get("/dash")
async def admin_dash(
    request: Request,
    media: list[str] | None = Query(None),
    is_admin=Depends(verify_token),
):
    media_proc = [
        {"name": os.path.basename(urlparse(m).path), "url": m} for m in media or []
    ]

    return templates.TemplateResponse(
        "dash.html", {"request": request, "media": media_proc}
    )


@router.post("/upmedia")
async def handle_upload(
    files: list[UploadFile] = File(...), is_admin=Depends(verify_token)
):

    urls = await AdminService().save_files(files)
    redirect_url = "/a/dash?media=" + "&media=".join(quote_plus(url) for url in urls)

    response = RedirectResponse(redirect_url, status_code=302)

    return response
