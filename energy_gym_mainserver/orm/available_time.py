from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from . import Base


class AvailableTime(Base):
    
    __tablename__ = 'available_time'

    code                = Column(Integer, primary_key=True, autoincrement=True)
    weektime            = Column(String, nullable=False)
    number_of_persons   = Column(Integer, nullable=False)
    month               = Column(String, nullable=False)

    entries             = relationship('Entry', uselist=False, back_populates='available_time')
