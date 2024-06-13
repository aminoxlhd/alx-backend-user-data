#!/usr/bin/env python3
"""
auth
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """_hash_password function"""
    hashed_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_bytes
