from typing import Type
from typing import Optional

from .converter import DTOConverter
from ..services import UsersService
from ..models import dto
from ..orm import User


class UserDBController:

    def __init__(self, service_type: Type[UsersService], converter: DTOConverter):
        self.service_type = service_type
        self.converter = converter

    
    def get_all(self, get_deleted: Optional[bool] = False) -> dto.UserList:
        with self.service_type() as service:
            return dto.UserList(
                data = [
                    self.converter.user_to_model(user)
                    for user in service.get_all(get_deleted)
                ]
            )
         

    def create(self, payload: dto.UserCreateRequest):
        with self.service_type() as service:
            service.create(
                User(**payload.data.dict())
            )
            service.commit()
