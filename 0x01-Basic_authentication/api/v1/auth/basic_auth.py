#!/usr/bin/env python3
""" Basic auth"""
import base64
import binascii
from typing import TypeVar, List
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """extract_base64_authorization_header function"""
        if (authorization_header is None or
                not isinstance(authorization_header, str) or
                not authorization_header.startswith("Basic")):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decode_base64_authorization_header function"""
        b64_auth_header = base64_authorization_header
        if b64_auth_header and isinstance(b64_auth_header, str):
            try:
                encode = b64_auth_header.encode('utf-8')
                base = base64.b64decode(encode)
                return base.decode('utf-8')
            except binascii.Error:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """extract_user_credentials function"""
        decoded_64 = decoded_base64_authorization_header
        if (decoded_64 and isinstance(decoded_64, str) and
                ":" in decoded_64):
            res = decoded_64.split(":", 1)
            return (res[0], res[1])
        return (None, None)

    def current_user(self, request=None) -> TypeVar('User'):
        """urrent_user function"""
        heade = self.authorization_header(request)
        b64header = self.extract_base64_authorization_header(heade)
        decoded = self.decode_base64_authorization_header(b64header)
        user_creds = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(*user_creds)
