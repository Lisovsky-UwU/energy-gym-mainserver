from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Token(Base):

    __tablename__ = 'tokens'

    id            = Column(Integer, primary_key=True, autoincrement=True)
    token         = Column(String(36), nullable=False, index=True)
    user          = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    create_time   = Column(DateTime, nullable=False, default=datetime.now)
    deleted       = Column(Boolean, default=False)

    users         = relationship('User', back_populates='tokens')
