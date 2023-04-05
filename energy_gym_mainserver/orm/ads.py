from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Ads(Base):
    
    __tablename__ = 'ads'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    create_time     = Column(DateTime, nullable=False, default=datetime.now)
    body            = Column(String, nullable=False)
    user            = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    deleted         = Column(Boolean, default=False)

    users           = relationship('User', back_populates='ads', uselist=False)
