from typing import Type
from typing import Optional

from ..services import UserDBService
from ..models import dto
from ..orm import User


class UserDBController:

    def __init__(self, service_type: Type[UserDBService]):
        self.service_type = service_type

    
    def get_all(self, get_deleted: Optional[bool] = False) -> dto.UserList:
        with self.service_type() as service:
            return dto.UserList(
                data = [
                    dto.UserModel.from_orm(user)
                    for user in service.get_all(get_deleted)
                ]
            )
         

    def create(self, payload: dto.UserCreateRequest) -> dto.UserModel:
        with self.service_type() as service:
            user = service.create(
                User(**payload.dict())
            )
            service.commit()

            return dto.UserModel.from_orm(user)
