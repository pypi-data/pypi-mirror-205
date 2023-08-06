from arkdata.database.cursor import sqlalchemy
from arkdata.database.table import Table
from sqlalchemy import Column, String, Integer, Boolean
from pathlib import Path
import os
import arkdata


class Command(sqlalchemy.db.Model, Table):
    admin_gamertag = Column(String(100), unique=False, nullable=True)
    player_gamertag = Column(String(100), unique=False, nullable=True)
    code = Column(String(500), unique=False, nullable=False)
    executed = Column(Boolean, unique=False, nullable=False, default=False)
    service_id = Column(String(100), unique=False, nullable=True, default=None)
    server_name = Column(String(200), unique=False, nullable=True)

    def __init__(
            self,
            admin_gamertag: str = None,
            player_gamertag: str = None,
            code: str = None,
            executed: bool = False,
            service_id: str = None,
            server_name: str = None,
    ):
        self.admin_gamertag = admin_gamertag    # Admin who executed the code
        self.player_gamertag = player_gamertag  # Player who requested the code
        self.code = code
        self.executed = executed
        self.service_id = service_id
        self.server_name = server_name

    @classmethod
    def seed_table(cls) -> None:
        dir = Path(os.path.dirname(arkdata.__file__))
        path = dir / Path('seeds/commands.json')
        super()._seed_table(path)

    @classmethod
    def queued_commands(cls, service_id: str) -> list:
        return cls.find_all_by(service_id=service_id, executed=False)

    @classmethod
    def completed_commands(cls, service_id: str) -> list:
        return cls.find_all_by(service_id=service_id, executed=True)

    @classmethod
    def player_commands(cls, gamertag: str) -> list:
        return cls.find_all_by(player_gamertag=gamertag)

    @classmethod
    def admin_commands(cls, gamertag: str) -> list:
        return cls.find_all_by(admin_gamertag=gamertag)

