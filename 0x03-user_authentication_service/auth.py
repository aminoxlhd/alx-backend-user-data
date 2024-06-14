#!/usr/bin/env python3
"""
auth
"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """
    Generate a new UUID and return it as a string.
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """
    Hash a password with bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """init function"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register_user function"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email, hashed_password.decode('utf-8'))
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """valid_login function"""
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                        password.encode("utf-8"),
                        user.hashed_password.encode("utf-8"))
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """create_session function"""
        try:
            user = self._db.find_user_by(email=email)
            new_session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=new_session_id)
            return new_session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """get_user_from_session_id function"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int):
        """destroy_session function"""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return

    def get_reset_password_token(self, email: str) -> str:
        """get_reset_password_token function"""
        try:
            user = self._db.find_user_by(email=email)
            new_session_id = _generate_uuid()
            self._db.update_user(user.id, reset_token=new_session_id)
            return new_session_id
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str):
        """update_password function"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id, password=password)
        except NoResultFound:
            raise ValueError()
