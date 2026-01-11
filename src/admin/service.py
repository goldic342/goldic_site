import hmac
import json
import hashlib
from config import settings
from datetime import datetime, timedelta, timezone


class AdminService:
    def __hash_password(self, password: str, salt: bytes, iter: int = 100_000) -> str:
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
            raise ValueError("Nuh uh")

        if not hmac.compare_digest(
            self.__hash_password(password, settings.ADMIN_PASSWORD_SALT.encode()),
            settings.ADMIN_PASSWORD_HASH,
        ):
            raise ValueError("Nuh uh")

        return self.__create_token()
