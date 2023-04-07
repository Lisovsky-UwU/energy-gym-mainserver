from typing import Type
from typing import List
from typing import Dict
from typing import Tuple
from typing import Optional

from ..exceptions import LogicError
from ..services import UserDBService
from ..models import dto
from ..orm import User


class UserDBController:

    def __init__(self, service_type: Type[UserDBService]):
        self.service_type = service_type

    
    def get_all(self, get_deleted: Optional[bool] = False) -> Tuple[dto.UserModel]:
        with self.service_type() as service:
            return tuple(
                dto.UserModel.from_orm(user)
                for user in service.get_all(get_deleted)
            )
         

    def get(self, user_id: int) -> dto.UserModel:
        with self.service_type() as service:
            user = service.get_by_id(user_id)

            if user is None:
                raise LogicError('Пользователь не найден')

            return dto.UserModel.from_orm(user)


    def create(self, payload: dto.UserCreateRequest) -> dto.UserModel:
        with self.service_type() as service:
            user = service.create(
                User(**payload.dict())
            )
            service.commit()

            return dto.UserModel.from_orm(user)


    def user_data_update(self, user_id: int, data: dto.UserDataUpdateRequest) -> dto.UserModel:
        with self.service_type() as service:
            user = service.get_by_id(user_id)
            
            service.update(self.__correlate_orm__(user, data))
            service.commit()

            return dto.UserModel.from_orm(user)


    def update_any_user_data(self, data: List[dto.UserAnyDataUpdateRequest]) -> Tuple[dto.UserModel]:
        with self.service_type() as service:
            result_list = list()

            for new_data in data:
                user = service.get_by_id(new_data.id)

                if user is not None:
                    result_list.append(
                        service.update(
                            self.__correlate_orm__(user, new_data)
                        )
                    )
            
            service.commit()

            return tuple(
                dto.UserModel.from_orm(user)
                for user in result_list
            )
        
    
    def delete_for_id_list(self, id_list: List[int]) -> Dict[int, str]:
        with self.service_type() as service:
            result_dict = dict()

            for user_id in id_list:
                user = service.get_by_id(user_id)

                if user is None or user.deleted:
                    result_dict[user_id] = 'Пользователь не найден'

                else:
                    service.delete(user)
                    result_dict[user_id] = 'Успешно'
            
            service.commit()

            return result_dict


    def __correlate_orm__(self, user: User, data: dto.UserDataUpdateRequest) -> User:
        if data.name is not None:
            user.name = data.name
        if data.group is not None:
            user.group = data.group
        if data.password is not None:
            user.password = data.password
        
        return user
