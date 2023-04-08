from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import Base
from ..models import VisitMark


class Visit(Base):
    
    __tablename__ = 'visits'

    id      = Column(Integer, primary_key=True, autoincrement=True)
    date    = Column(Date, nullable=False)
    entry   = Column(Integer, ForeignKey('entries.id'), nullable=False, index=True)
    mark    = Column(Integer, nullable=False, default=VisitMark.PASS)
    deleted = Column(Boolean, default=False)

    entries = relationship('Entry', back_populates='visits', uselist=False)
