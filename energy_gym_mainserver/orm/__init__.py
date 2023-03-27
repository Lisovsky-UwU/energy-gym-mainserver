from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import create_session

from ..configmodule import config


engine = create_engine(config.postgre.connect_str, future=True)
Base = declarative_base(bind=engine)


def session_factory(**kwargs):
    return create_session(
        bind=engine,
        autocommit=False,
        autoflush=False,
        future=True,
        **kwargs
    )


from .available_time import AvailableTime
from .entry import Entry
from .user import User
