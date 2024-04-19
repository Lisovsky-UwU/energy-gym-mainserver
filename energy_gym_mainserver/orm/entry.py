from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from . import Base
from .mixins import BaseMixin


class Entry(BaseMixin, Base):
    
    __tablename__ = 'entries'

    create_time    : Mapped[datetime] = mapped_column(default=datetime.now)
    selected_time  : Mapped[int] = mapped_column(ForeignKey('available_time.id'), index=True)
    user           : Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)

    available_time : Mapped['AvailableTime'] = relationship(back_populates='entries', uselist=False)
    user_model     : Mapped['User'] = relationship(back_populates='entries', uselist=False)
    visits         : Mapped['Visit'] = relationship(back_populates='entry_model', uselist=True)


from .available_time import AvailableTime
from .user import User
from .visit import Visit
