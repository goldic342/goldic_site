from starlette.types import ASGIApp, Receive, Scope, Send

Headers = list[tuple[bytes, bytes]]


class RealIPMiddleware:
    """
    Middleware that updates the ASGI scope based on proxy headers
    set by reverse proxy (X-Real-IP, X-Forwarded-For, X-Forwarded-Proto, Host).
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        headers = dict(scope.get("headers", []))

        if b"x-real-ip" in headers:
            ip = headers[b"x-real-ip"].decode("latin1")
            scope["client"] = (ip, scope["client"][1])

        if b"x-forwarded-proto" in headers:
            scheme = headers[b"x-forwarded-proto"].decode("latin1")
            scope["scheme"] = scheme

        await self.app(scope, receive, send)
