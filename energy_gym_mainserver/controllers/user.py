from typing import Type, List, Dict, Tuple, Union, Iterable
from loguru import logger

from ..exceptions import LogicError
from ..services import UserDBService
from ..models import dto
from ..orm import User


class UserDBController:

    def __init__(self, service_type: Type[UserDBService]):
        self.service_type = service_type


    def get_any(
        self,
        groups: Union[Iterable[str], str] = (),
        roles: Union[Iterable[str], str] = (),
        deleted: bool = False,
        **kwargs
    ) -> Tuple[dto.UserModelExtended]:
        if isinstance(groups, str):
            groups = [groups]
        
        if isinstance(roles, str):
            roles = [roles]

        with self.service_type() as service:
            return self.__to_tuple_extended_model__(
                service.get_for_filter(
                    groups  = groups,
                    roles   = roles,
                    deleted = deleted
                )
            )


    def get(self, user_id: int) -> dto.UserModel:
        with self.service_type() as service:
            user = service.get_by_id(user_id)

            if user is None:
                raise LogicError('Пользователь не найден')

            return dto.UserModel.from_orm(user)


    def create(self, payload: Iterable[dto.UserCreateRequest]) -> Tuple[dto.UserModel]:
        with self.service_type() as service:
            result_list = service.create_for_iter(
                User(**user.dict())
                for user in payload
            )
            service.commit()

            logger.trace(f'Были созданы пользователи: {list(user.id for user in result_list)}')
            return self.__to_tuple_model__(result_list)


    def user_data_update(self, user_id: int, data: dto.UserDataUpdateRequest) -> dto.UserModel:
        with self.service_type() as service:
            user = service.get_by_id(user_id)
            
            service.update(self.__correlate_orm__(user, data))
            service.commit()

            logger.trace(f'Были обновлены данные для пользователя с ID {user_id}: {data.dict()}')
            return dto.UserModel.from_orm(user)



    def user_password_update(self, user_id: int, data: dto.UserPasswordUpdateRequest) -> bool:
        with self.service_type() as service:
            user = service.get_by_id(user_id)

            if data.old_password != user.password:
                raise LogicError('Неверный прежний пароль')
        
            user.password = data.new_password
            service.update(user)
            service.commit()

            logger.trace(f'Был обновлен пароль для пользователя с ID {user_id}')
            return True


    def update(self, data: List[dto.UserAnyDataUpdateRequest]) -> Tuple[dto.UserModel]:
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

            logger.trace(f'Были обновлены данные для пользователей: {list(user.id for user in result_list)}')
            return self.__to_tuple_model__(result_list)
        
    
    def delete(self, id_list: List[int]) -> Dict[int, str]:
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

            logger.trace(f'Удаление пользователей: {result_dict}')
            return result_dict


    def __correlate_orm__(self, user: User, data: dto.UserDataUpdateRequest) -> User:
        if data.firstname is not None:
            user.firstname = data.firstname
        if data.secondname is not None:
            user.secondname = data.secondname
        if data.surname is not None:
            user.surname = data.surname
        if data.group is not None:
            user.group = data.group
        
        return user


    def __to_tuple_model__(self, data: Iterable[User]) -> Tuple[dto.UserModel]:
        return tuple(
            dto.UserModel.from_orm(user)
            for user in data
        )

    def __to_tuple_extended_model__(self, data: Iterable[User]) -> Tuple[dto.UserModelExtended]:
        return tuple(
            dto.UserModelExtended.from_orm(user)
            for user in data
        )
