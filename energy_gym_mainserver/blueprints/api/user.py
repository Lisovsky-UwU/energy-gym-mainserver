from flask import Blueprint, request
from loguru import logger
from sqlalchemy import and_
from sqlalchemy.orm import Session

from .handlers import format_response
from ...orm import SessionCtx, User
from ...models import dto, UserRole
from ...utils import generate_hid
from ...exceptions import DataBaseException, LogicError


user_bl = Blueprint('user', 'user')


def get_user_from_db(session: Session, user_id: int) -> User:
    user: User | None = session.query(User).get( user_id )
    if user is None:
        raise DataBaseException(f'Пользователь с id={user_id} не найден')
    
    return user


def get_auth_from_db(session: Session) -> User:
    return get_user_from_db(session, int( request.headers.get('user-id') ))


def update_user_data(user: User, upd_data: dto.UserDataUpdateRequest):
    if upd_data.firstname:
        user.firstname = upd_data.firstname
    if upd_data.secondname:
        user.secondname = upd_data.secondname
    if upd_data.surname:
        user.surname = upd_data.surname
    if upd_data.group:
        user.group = upd_data.group


@user_bl.post('/create')
@format_response
def create_user():
    data = dto.UserCreateRequest.parse_obj( request.json )
    with SessionCtx() as session:
        user = User(
            student_card = data.studentCard,
            firstname    = data.firstname,
            secondname   = data.secondname,
            surname      = data.surname,
            group        = data.group,
            hid          = generate_hid(data.studentCard, data.password),
            role         = UserRole.STUDENT.name,
        )
        session.add(user)
        logger.success(f'Создан новоый пользователь id={user} пользователем с id={request.headers.get("user-id")}')
        
        return dto.UserResponse.from_orm(user)


@user_bl.get('/get')
@format_response
def get_user():
    _filter = True
    data = dto.UserGetRequest.parse_obj( request.json )

    if data.role is not None:
        _filter = and_(_filter, User.role == data.role)

    with SessionCtx() as session:
        return [
            dto.UserResponse.from_orm(user)
            for user in session.query(User).where(_filter).all()
        ]


@user_bl.put('/edit')
@format_response
def edit_user():
    data = dto.UserDataUpdateRequest.parse_obj( request.json )

    with SessionCtx() as session:
        user = get_auth_from_db(session)
        update_user_data(user, data)

        session.commit()
        return dto.UserBaseResponse.from_orm(user)


@user_bl.put('/edit-password')
@format_response
def edit_password():
    data = dto.UserPasswordUpdateRequest.parse_obj( request.json )

    with SessionCtx() as session:
        user = get_auth_from_db(session)
        if generate_hid(user.student_card, data.oldPassword) != user.hid:
            raise LogicError('Неверный старый пароль')

        user.hid = generate_hid(user.student_card, data.newPassword)
        session.commit()

        logger.success(f'Изменен пароль для пользователя {user.id}')

    return dto.SuccessResponse()


@user_bl.put('/edit-any')
@format_response
def edit_any_entries():
    data = dto.UserAnyDataUpdateRequest.parse_obj( request.json )

    with SessionCtx() as session:
        user = get_user_from_db(session, data.id)

        update_user_data(user, data)
        if data.newPassword:
            user.hid = generate_hid(user.student_card, data.newPassword)
            logger.success(f'Был изменен пароль для пользователя с id={data.id}')
        
        return dto.UserResponse.from_orm(user)


@user_bl.delete('/delete-any')
@format_response
def delete_any_entries():
    data = dto.DeleteRequest(request.json)

    with SessionCtx() as session:
        user = get_user_from_db(session, data.id)
        user.deleted = True

        session.commit()

    logger.success(f'Удален пользователь с id={data.id}')
    return dto.SuccessResponse()
