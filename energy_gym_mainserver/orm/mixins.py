from sqlalchemy.orm import Mapped, mapped_column


class BaseMixin:

    id          : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    deleted     : Mapped[bool] = mapped_column(server_default='false')
