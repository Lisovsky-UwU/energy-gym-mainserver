from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

from . import Base


class User(Base):

    __tablename__ = 'users'

    id            = Column(Integer, primary_key=True, autoincrement=True)
    student_card  = Column(Integer, nullable=False)
    name          = Column(String(50), nullable=False)
    group         = Column(String(20), nullable=False)
    password      = Column(String(25), nullable=False)
    role          = Column(String(15), nullable=False)
    deleted       = Column(Boolean, default=False)

    entries       = relationship('Entry', uselist=False, back_populates='users')
