from .abc import BaseService
from ..orm import User


class UserDBService(BaseService[User]):
    ...
