#!/usr/bin/env python3
"""
db"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class"""

    def __init__(self) -> None:
        """init function"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """_session function"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        "add_user function"
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by specified attributes.

        Raises:
            error: NoResultFound: When no results are found.
            error: InvalidRequestError: When invalid query arguments are passed

        Returns:
            User: First row found in the `users` table.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise
        return None

    def update_user(self, user_id: int, **kwargs) -> None:
        """update_user function"""
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid argument: {key}")
            setattr(user, key, value)

        self._session.commit()
