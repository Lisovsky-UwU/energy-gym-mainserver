from typing import List
from sqlalchemy.orm import relationship, Mapped, mapped_column

from . import Base
from .mixins import BaseMixin
from ..utils import get_next_month


class AvailableTime(BaseMixin, Base):
    
    __tablename__ = 'available_time'

    weekday           : Mapped[int]
    time              : Mapped[str]
    number_of_persons : Mapped[int]
    month             : Mapped[str] = mapped_column(default=get_next_month, index=True)

    entries           : Mapped[List['Entry']] = relationship(back_populates='available_time', uselist=True)


    @property
    def not_deleted_entries(self):
        return list(entry for entry in self.entries if not entry.deleted)


from .entry import Entry
