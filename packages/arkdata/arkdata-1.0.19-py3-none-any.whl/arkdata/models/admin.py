from __future__ import annotations
from sqlalchemy import Column, String, DateTime
from arkdata.database.cursor import sqlalchemy
from arkdata.database.table import Table
from arkdata import models
from pathlib import Path
import arkdata
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import bcrypt
import base64
from datetime import datetime


class Admin(sqlalchemy.db.Model, Table):
    xuid = Column(String(100), nullable=False, unique=True)
    nitrado_api_key = Column(String(500), nullable=True)
    subscription_start = Column(DateTime, nullable=False, default=datetime.now())
    subscription_end = Column(DateTime, nullable=False, default=datetime.now())

    @classmethod
    def cipher(cls, password: str) -> Fernet:
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=None,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(hkdf.derive(password.encode()))
        return Fernet(key)

    @classmethod
    def encrypt(cls, content: str, password: str):
        if not isinstance(content, str):
            raise Exception("Content must be a string to encrypt")
        cipher = cls.cipher(password)
        return cipher.encrypt(content.encode()).decode()

    @classmethod
    def decrypt(cls, content: str, password: str) -> str:
        cipher = cls.cipher(password)
        return cipher.decrypt(content.encode()).decode()

    def __init__(self, xuid=None, nitrado_api_key=None, subscription_start=None, subscription_end=None):
        self.xuid: str = xuid
        self.subscription_start: datetime = subscription_start
        self.subscription_end: datetime = subscription_end
        self.nitrado_api_key = nitrado_api_key

    @classmethod
    def seed_table(cls) -> None:
        dir = Path(os.path.dirname(arkdata.__file__))
        path = dir / Path('seeds/admins.json')
        super()._seed_table(path)

    def update_subscription_start(self, month: int, day: int, year: int):
        self(subscription_start=datetime(year=year, month=month, day=day))

    def update_subscription_end(self, month: int, day: int, year: int):
        self(subscription_end=datetime(year=year, month=month, day=day))

    def subscription(self, start: DateTime = None, end: DateTime = None):
        subscription_start = start or self.subscription_start or datetime.now()
        subscription_end = end or self.subscription_end or datetime.now()
        self(subscription_start=subscription_start, subscription_end=subscription_end)
