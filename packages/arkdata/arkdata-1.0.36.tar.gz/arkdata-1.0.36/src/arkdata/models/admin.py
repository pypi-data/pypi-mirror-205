from __future__ import annotations
from sqlalchemy import Column, String, DateTime
from ..database.cursor import sqlalchemy
from ..database.table import Table
from .. import models
from pathlib import Path
import arkdata
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import base64
from datetime import datetime


class Admin(sqlalchemy.db.Model, Table):
    xuid = Column(String(100), nullable=False, unique=True)
    nitrado_api_key = Column(String(500), nullable=True)
    subscription_start = Column(DateTime, default=datetime.now)
    subscription_end = Column(DateTime, default=datetime.now)

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
    def encrypt(cls, content: str, password: str) -> str:
        cipher = cls.cipher(password)
        return cipher.encrypt(content.encode()).decode()

    @classmethod
    def decrypt(cls, content: str, password: str) -> str:
        cipher = cls.cipher(password)
        return cipher.decrypt(content.encode()).decode()

    @classmethod
    def seed_table(cls) -> None:
        dir = Path(os.path.dirname(arkdata.__file__))
        path = dir / Path('seeds/admins.json')
        super()._seed_table(path)

    def __init__(self, xuid=None, nitrado_api_key=None, subscription_start=None, subscription_end=None):
        self.xuid: str = xuid
        self.subscription_start: datetime = subscription_start or datetime.now()
        self.subscription_end: datetime = subscription_end or datetime.now()
        self.nitrado_api_key = nitrado_api_key

    def user(self) -> models.User | Table:
        return models.User.find_by(xuid=self.xuid)

    def update_subscription_start(self, month: int, day: int, year: int) -> None:
        self(subscription_start=datetime(year=year, month=month, day=day))

    def update_subscription_end(self, month: int, day: int, year: int) -> None:
        self(subscription_end=datetime(year=year, month=month, day=day))

    def update_subscription(self, start: datetime, end: datetime) -> None:
        subscription_start = start or self.subscription_start or datetime.now()
        subscription_end = end or self.subscription_end or datetime.now()
        self(subscription_start=subscription_start, subscription_end=subscription_end)

    def has_active_subscription(self) -> bool:
        if self.subscription_start is None or self.subscription_end is None:
            return False
        if self.subscription_start >= self.subscription_end:
            return False
        return self.subscription_start <= datetime.now() < self.subscription_end

