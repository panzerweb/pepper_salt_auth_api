import hashlib
import os
import base64

def hash_password(password: str, salt: bytes = None, pepper: bytes = b"") -> tuple[str, str]:
    """
    Hash password with salt + pepper using SHA-256
    Returns: (hashed_password, salt)
    """
    if salt is None:
        salt = os.urandom(16)

    combined = salt + password.encode() + pepper
    hashed = hashlib.sha256(combined).digest()
    hashed_b64 = base64.b64encode(hashed).decode()
    salt_b64 = base64.b64encode(salt).decode()
    return hashed_b64, salt_b64


def verify_password(password: str, hashed_password_b64: str, salt_b64: str, pepper: bytes = b"") -> bool:
    salt = base64.b64decode(salt_b64)
    combined = salt + password.encode() + pepper
    hashed = hashlib.sha256(combined).digest()
    hashed_b64 = base64.b64encode(hashed).decode()
    return hashed_b64 == hashed_password_b64