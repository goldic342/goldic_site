import hashlib
import warnings
from pydantic_settings import BaseSettings, SettingsConfigDict
from os import path


def _assert_sha256_hex(value: str) -> None:
    try:
        raw = bytes.fromhex(value)
    except ValueError:
        raise RuntimeError("ADMIN_PASSWORD_HASH is not valid hex")

    if len(raw) != hashlib.sha256().digest_size:
        raise RuntimeError("ADMIN_PASSWORD_HASH is not SHA-256 (expected 32 bytes)")


class Settings(BaseSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD_HASH: str  # sha256 hex
    ADMIN_PASSWORD_SALT: str

    TOKEN_SECRET: str

    DATA_DIR: str = "./data"

    MAX_FILESIZE: int = 10 * 1024 * 1024
    MAX_FILES: int = 5

    IS_PROD: bool = True

    model_config = SettingsConfigDict(
        env_file=path.join(path.dirname(path.abspath(__file__)), "..", ".env")
    )

    def __init__(self, **values):
        super().__init__(**values)

        _assert_sha256_hex(self.ADMIN_PASSWORD_HASH)

        if len(self.ADMIN_PASSWORD_SALT) < 16:
            warnings.warn(
                "ADMIN_PASSWORD_SALT is weak (<16 chars). Use a random salt.",
                RuntimeWarning,
            )


settings = Settings()  # type: ignore
