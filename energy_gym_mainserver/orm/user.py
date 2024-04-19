from typing import List
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from . import Base
from .mixins import BaseMixin
from ..models import UserRole


class User(BaseMixin, Base):

    __tablename__ = 'users'

    student_card : Mapped[int] = mapped_column(unique=True, index=True)
    firstname    : Mapped[str]
    secondname   : Mapped[str]
    surname      : Mapped[str]
    group        : Mapped[str]
    hid          : Mapped[str]
    role         : Mapped[UserRole] = mapped_column(Enum(UserRole))

    ads          : Mapped['Ads'] = relationship(back_populates='user_model',  uselist=True)
    entries      : Mapped[List['Entry']] = relationship(back_populates='user_model',  uselist=True)


from .ads import Ads
from .entry import Entry
