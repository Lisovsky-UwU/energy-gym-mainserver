from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

from . import Base
from ..configmodule import config


def cur_month_fabric() -> str:
    return datetime.now().strftime(config.common.av_month_format)


class AvailableTime(Base):
    
    __tablename__ = 'available_time'

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    weektime            = Column(String, nullable=False)
    number_of_persons   = Column(Integer, nullable=False)
    month               = Column(String, nullable=False, default=cur_month_fabric, index=True)
    deleted             = Column(Boolean, default=False)

    entries             = relationship('Entry', back_populates='available_time', uselist=True)
