from pydantic_settings import BaseSettings, SettingsConfigDict
from os import path


class Settings(BaseSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD_HASH: str  # PBKDF2
    ADMIN_PASSWORD_SALT: str

    TOKEN_SECRET: str

    DATA_DIR: str = "./data"

    MAX_FILESIZE: int = 10 * 1024 * 1024
    MAX_FILES: int = 5

    IS_PROD: bool = True

    model_config = SettingsConfigDict(
        env_file=path.join(path.dirname(path.abspath(__file__)), "..", ".env")
    )


settings = Settings()  # type: ignore
