from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from admin.service import AdminService

router = APIRouter(prefix="/a")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def admin(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def admin_login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    token = AdminService().login(username, password)

    response.set_cookie(key="toooken", value=token)

    return RedirectResponse("/a/dash")
