from pydantic_settings import BaseSettings, SettingsConfigDict
from os import path


class Settings(BaseSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD_HASH: str  # PBKDF2
    ADMIN_PASSWORD_SALT: str

    TOKEN_SECRET: str

    model_config = SettingsConfigDict(
        env_file=path.join(path.dirname(path.abspath(__file__)), "..", ".env")
    )


settings = Settings()  # type: ignore
