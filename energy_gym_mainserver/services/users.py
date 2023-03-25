from .abc import BaseService
from ..orm import User


class UsersService(BaseService[User]):
    ...
