import hashlib
import os
import base64

def hash_password(password: str, salt: bytes = None, pepper: bytes = b"") -> tuple[str, str]:
    """
    Hash password with salt + pepper using SHA-256
    Returns: (hashed_password, salt)
    """
    # Generate a random 16-byte salt if not provided
    if salt is None:
        salt = os.urandom(16)

    # Combine salt + password + pepper for hashing
    combined = salt + password.encode() + pepper

    # Perform SHA-256 hashing
    hashed = hashlib.sha256(combined).digest()

    # Encode hash and salt to base64 for safe storage as strings
    hashed_b64 = base64.b64encode(hashed).decode()
    salt_b64 = base64.b64encode(salt).decode()

    # Return encoded hash and salt
    return hashed_b64, salt_b64


def verify_password(password: str, hashed_password_b64: str, salt_b64: str, pepper: bytes = b"") -> bool:
    # Decode the stored salt from base64 back to bytes
    salt = base64.b64decode(salt_b64)

    # Recreate the original hash input (salt + password + pepper)
    combined = salt + password.encode() + pepper

    # Hash the combined value using SHA-256
    hashed = hashlib.sha256(combined).digest()

    # Encode the computed hash to base64
    hashed_b64 = base64.b64encode(hashed).decode()

    # Compare computed hash with stored hash
    return hashed_b64 == hashed_password_b64