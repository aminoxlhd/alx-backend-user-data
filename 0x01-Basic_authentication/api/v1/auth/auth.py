#!/usr/bin/env python3
"""manage the API authentication"""
from typing import List, TypeVar
from flask import request


class Auth():
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth function"""
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header function"""
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user function"""
        return None
