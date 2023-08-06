from __future__ import annotations
from sqlalchemy import Column, String
from ..database.cursor import sqlalchemy
from ..database.table import Table
from pathlib import Path
import os
import arkdata
from .. import models
import bcrypt


def random_xuid():
    from random import randint
    return f"temporary_xuid_{randint(1, 10000)}"


class User(sqlalchemy.db.Model, Table):
    xuid = Column(String(100), nullable=False, unique=True)
    gamertag = Column(String(100))
    password_digest = Column(String(100))

    def __init__(self, xuid=None, gamertag=None, password_digest=None):
        self.xuid: str = xuid
        self.gamertag: str = gamertag
        self.password_digest: str = password_digest

    @classmethod
    def seed_table(cls) -> None:
        dir = Path(os.path.dirname(arkdata.__file__))
        path = dir / Path('seeds/users.json')
        super()._seed_table(path)
        session_token = cls.create_user("TEST_GAMERTAG", "TEST_PASSWORD")
        session = models.Session.find_by(session_token=session_token)
        user = User.find_by(xuid=session.xuid)
        user(xuid="TEST_XUID")

    @classmethod
    def create_user(cls, gamertag: str, password: str) -> str | None:
        """Returns the session token"""
        if User.find_by(gamertag=gamertag.lower()) is not None:
            return
        xuid = random_xuid()
        password_digest = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = cls(xuid=xuid, gamertag=gamertag, password_digest=password_digest)
        user.create()
        models.Account(xuid=xuid).create()
        session = models.Session(xuid=xuid).create()
        return session.new_session_token()

    @classmethod
    def login(cls, gamertag: str, password: str) -> str | None:
        """Returns the session token"""
        user = models.User.find_by(gamertag=gamertag)
        if user is None:
            return
        is_password_valid = bcrypt.checkpw(password.encode(), user.password_digest.encode())
        if not is_password_valid:
            return
        session = user.session()
        return session.new_session_token()

    def change_password(self, password: str) -> bool:
        if not isinstance(password, str):
            return False
        password_digest = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self(password_digest=password_digest)
        return True

    def session(self) -> models.Session:
        return models.Session.find_by(xuid=self.xuid)

    def account(self) -> models.Account:
        return models.Account.find_by(xuid=self.xuid)

    def cart_items(self) -> list[models.CartItem]:
        return models.CartItem.find_all_by(xuid=self.xuid)

    def orders_by_id(self, order_number: str) -> list[models.OrderItem]:
        return models.OrderItem.find_all_by(xuid=self.xuid, order_number=order_number)

    def is_admin(self) -> bool:
        return models.Admin.find_by(xuid=self.xuid) is not None
