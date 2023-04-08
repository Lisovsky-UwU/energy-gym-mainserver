from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

from . import Base
from ..utils import get_next_month


class AvailableTime(Base):
    
    __tablename__ = 'available_time'

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    weekday             = Column(Integer, nullable=False)
    time                = Column(String, nullable=False)
    number_of_persons   = Column(Integer, nullable=False)
    month               = Column(String, nullable=False, default=get_next_month, index=True)
    deleted             = Column(Boolean, default=False)

    entries             = relationship('Entry', back_populates='available_time', uselist=True)


    @property
    def not_deleted_entries(self):
        return list(entry for entry in self.entries if not entry.deleted)
