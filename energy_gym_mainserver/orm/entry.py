from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Entry(Base):
    
    __tablename__ = 'entries'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    create_time     = Column(DateTime, nullable=False, default=datetime.now)
    selected_time   = Column(Integer, ForeignKey('available_time.id'), nullable=False, index=True)
    user            = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    deleted         = Column(Boolean, default=False)

    available_time  = relationship('AvailableTime', back_populates='entries')
    users           = relationship('User', back_populates='entries')
