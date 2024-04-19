import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from . import Base
from .mixins import BaseMixin
from ..models import VisitMark


class Visit(BaseMixin, Base):
    
    __tablename__ = 'visits'

    date        : Mapped[datetime.date] = mapped_column(index=True)
    entry       : Mapped[int] = mapped_column(ForeignKey('entries.id'), index=True)
    mark        : Mapped[int] = mapped_column(default=VisitMark.PASS)

    entry_model : Mapped['Entry'] = relationship(back_populates='visits', uselist=False)


from .entry import Entry
