from fastapi import HTTPException, Request

from admin.service import AdminService


def verify_token(request: Request):
    token = request.cookies.get("toooken")

    if not token:
        raise HTTPException(status_code=401, detail="Deniend :(")

    if not AdminService().verify_token(token):

        raise HTTPException(status_code=401, detail="Deniend :(")

    return True
