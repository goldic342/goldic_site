import hmac
import re
from typing import Literal
import os
import json
import hashlib
from pathlib import Path
from admin.config import admin_settings

from fastapi import UploadFile
from blog.service import BlogService
from config import settings
from datetime import datetime, timedelta, timezone

from exceptions import DetailedError


class AdminService:

    def hash_password(self, password: str, salt: bytes, iter: int = 100_000) -> str:
        hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iter)

        return hash.hex()

    def __create_token(self) -> str:
        data = {
            "expiry": (datetime.now(timezone.utc) + timedelta(hours=24)).timestamp()
        }
        data = json.dumps(data).encode().hex()

        sign = hmac.new(
            settings.TOKEN_SECRET.encode(), data.encode(), hashlib.sha256
        ).hexdigest()

        return f"{sign}.{data}"

    def verify_token(self, token) -> bool:
        try:
            sign, data = token.split(".")
        except ValueError:
            return False

        expected_sign = hmac.new(
            settings.TOKEN_SECRET.encode(), data.encode(), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(sign, expected_sign):
            return False

        try:
            data = json.loads(bytes.fromhex(data))
        except (json.decoder.JSONDecodeError, TypeError):
            return False

        expiry = data.get("expiry", 0)
        try:
            is_expired = datetime.fromtimestamp(expiry, tz=timezone.utc) < datetime.now(
                timezone.utc
            )
        except (TypeError, ValueError):
            return False

        if is_expired:
            return False

        return True

    def login(self, username: str, password: str) -> str:
        if not hmac.compare_digest(username, settings.ADMIN_USERNAME):
            raise DetailedError("Wrong guess!")

        if not hmac.compare_digest(
            self.hash_password(password, settings.ADMIN_PASSWORD_SALT.encode()),
            settings.ADMIN_PASSWORD_HASH,
        ):
            raise DetailedError("Wrong guess!")

        return self.__create_token()

    def __check_file(self, file: UploadFile, file_type: Literal["img", "md"]) -> bool:
        allowed_mime = (
            admin_settings.IMG_MIME if file_type == "img" else admin_settings.MD_MIME
        )

        if (file.size or 0) > settings.MAX_FILESIZE:  # Redundant
            raise DetailedError("Too much", "I can't handle this!")

        if file.size == 0:
            return False

        if file.content_type not in allowed_mime:
            raise DetailedError("Can't do that!", "I don't like files like that.")

        return True

    def __normalize_filename(self, filename: str) -> str:
        filename = filename.strip()
        filename = filename.replace(" ", "_")
        filename = re.sub(r"[^A-Za-z0-9._\-!+]", "", filename)
        return filename  # type: ignore

    async def __check_md(
        self, file: UploadFile
    ) -> tuple[list[str], bytes, dict] | tuple[None, None, None]:
        data = bytearray()

        while True:
            chunk = await file.read(8192)
            if not chunk:
                break
            data += chunk
            if len(data) > settings.MAX_FILESIZE:
                raise DetailedError("Too much", "I can't handle this!")

        if not data:
            return None, None  # empty

        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            raise DetailedError("Invalid encoding", "Markdown must be UTF-8 encoded!!")

        lines = text.splitlines(keepends=True)

        meta, body = BlogService().get_meta(lines)
        if not meta or not body:
            raise DetailedError(
                "Meta is wrong!",
                "Ensure meta: name, generic_name, publish_date, description",
            )

        return lines, bytes(data), meta

    async def save_files(
        self,
        files: list[UploadFile],
        file_type: Literal["img", "md"],
    ) -> list[str]:
        if len(files) > settings.MAX_FILES:
            raise DetailedError("Too much", "I can't handle this!")

        urls: list[str] = []

        if file_type == "img":
            base_dir = Path(settings.DATA_DIR) / "media"
            url_prefix = "/up/media/"
        elif file_type == "md":
            base_dir = Path(settings.DATA_DIR) / "md"
            url_prefix = "/up/md/"

        base_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            if not self.__check_file(file, file_type):
                continue

            if file_type == "md":
                lines, raw, meta = await self.__check_md(file)
                if not lines or not raw or not meta:
                    continue

                generic = meta["generic_name"].strip()

                filename = self.__normalize_filename(generic) + ".md"
                data = raw

            else:
                name = os.path.basename(file.filename or "")
                if not name:
                    name = f"file_{os.urandom(10).hex()}"

                filename = self.__normalize_filename(name)
                data = await file.read()

            f_path = base_dir / filename
            if f_path.exists():
                raise DetailedError("Too redundant!", "File already exists")

            with open(f_path, "wb") as f:
                f.write(data)

            urls.append(f"{url_prefix}{filename}")

        return urls
