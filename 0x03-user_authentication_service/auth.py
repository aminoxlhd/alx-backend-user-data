#!/usr/bin/env python3
"""
auth
"""
import bcrypt
from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register_user function"""
        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f"User {email} already exists")

        hashed_password = _hash_password(password)
        user = User(email=email, hashed_password=hashed_password.decode())
        self._db.add_user(user.email, user.hashed_password)
        return user


def _hash_password(password: str) -> bytes:
    """_hash_password function"""
    hashed_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_bytes
