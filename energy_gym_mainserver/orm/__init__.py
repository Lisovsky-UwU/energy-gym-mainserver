from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import create_session

from ..configmodule import config


engine = create_engine(config.postgre.connect_str, future=True)
_base = declarative_base(bind=engine)


class Base(_base):

    deleted = Column(Boolean, default=False)


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
