from getpass import getpass
from secrets import token_urlsafe
import hashlib


def hash_password(password: str, salt: bytes, iter: int = 100_000) -> str:
    hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iter)

    return hash.hex()


if __name__ == "__main__":
    password = getpass("Password: ")
    salt = input("Salt ('Enter' to auto generate): ")

    if not salt:
        salt = token_urlsafe()

    hash = hash_password(password, salt.encode())

    print(f"SHA256 HASH: {hash}")
    print(f"Salt: {salt}")
