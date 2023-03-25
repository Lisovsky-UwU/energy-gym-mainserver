from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Entry(Base):
    
    __tablename__ = 'entries'

    code            = Column(Integer, primary_key=True, autoincrement=True)
    create_time     = Column(DateTime, nullable=False)
    selected_time   = Column(Integer, ForeignKey('available_time.code'), nullable=False, index=True)
    user            = Column(Integer, ForeignKey('users.code'), nullable=False, index=True)

    available_time  = relationship('AvailableTime', back_populates='entries')
    users           = relationship('User', back_populates='entries')
