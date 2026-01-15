from getpass import getpass
from random import randbytes
import hashlib


def hash_password(password: str, salt: bytes, iter: int = 100_000) -> str:
    hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iter)

    return hash.hex()


if __name__ == "__main__":
    password = getpass("Password: ")
    salt = input("Salt ('Enter' to auto generate): ")

    if not salt:
        salt = randbytes(24).hex()

    hash = hash_password(password, salt.encode())

    print(f"SHA256 HASH: {hash}")
    print(f"Salt: {salt}")
