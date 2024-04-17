from sqlalchemy import Column, String, Integer, Boolean, Text
from sqlalchemy.orm import relationship

from . import Base


class User(Base):

    __tablename__ = 'users'

    id            = Column(Integer, primary_key=True, autoincrement=True)
    student_card  = Column(Integer, nullable=False, unique=True, index=True)
    firstname     = Column(String(30), nullable=False)
    secondname    = Column(String(30), nullable=False)
    surname       = Column(String(30), nullable=False, default='')
    group         = Column(String(20), nullable=False)
    hid           = Column(Text, nullable=False)
    role          = Column(String(15), nullable=False, index=True)
    deleted       = Column(Boolean, default=False)

    ads           = relationship('Ads', back_populates='users',  uselist=True)
    entries       = relationship('Entry', back_populates='users',  uselist=True)
