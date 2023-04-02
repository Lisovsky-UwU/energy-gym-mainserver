from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

from . import Base


class User(Base):

    __tablename__ = 'users'

    id            = Column(Integer, primary_key=True, autoincrement=True)
    student_card  = Column(Integer, nullable=False, unique=True, index=True)
    name          = Column(String(70), nullable=False)
    group         = Column(String(20), nullable=False)
    password      = Column(String(60), nullable=False)
    role          = Column(String(15), nullable=False, index=True)
    deleted       = Column(Boolean, default=False)

    ads           = relationship('Ads', uselist=False, back_populates='users')
    tokens        = relationship('Token', uselist=False, back_populates='users')
    entries       = relationship('Entry', uselist=False, back_populates='users')
