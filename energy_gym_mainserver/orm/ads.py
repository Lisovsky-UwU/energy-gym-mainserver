from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from . import Base
from .mixins import BaseMixin


class Ads(BaseMixin, Base):
    
    __tablename__ = 'ads'

    create_time : Mapped[datetime] = mapped_column(default=datetime.now)
    body        : Mapped[str]
    user        : Mapped[int] = mapped_column(ForeignKey('users.id'))

    user_model  : Mapped['User'] = relationship(back_populates='ads', uselist=False)


from .user import User
