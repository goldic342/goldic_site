from admin.service import AdminService
from getpass import getpass
from random import randbytes

if __name__ == "__main__":
    password = getpass("Password: ")
    salt = input("Salt ('Enter' to auto generate): ")

    if not salt:
        salt = randbytes(24).hex()

    hash = AdminService().hash_password(password, salt.encode())

    print(f"SHA256 HASH: {hash}")
    print(f"Salt: {salt}")
