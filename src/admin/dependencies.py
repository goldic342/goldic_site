from fastapi import Request
from exceptions import DetailedError

from admin.service import AdminService


def verify_token(request: Request):
    token = request.cookies.get("toooken")

    if not token:
        raise DetailedError("Denied :(", "Maybe you shouldn't do this?")

    if not AdminService().verify_token(token):
        raise DetailedError("Denied :(", "There is no point of doing this!")

    return True
