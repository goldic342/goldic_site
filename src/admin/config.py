from pydantic_settings import BaseSettings


class AdminSettings(BaseSettings):
    IMG_MIME: set[str] = {"image/png", "image/jpeg", "image/webp", "image/gif"}
    MD_MIME: set[str] = {"text/markdown", "text/plain"}

    WINDOW: int = 60
    MAX_REQS: int = 3


admin_settings = AdminSettings()
