from loguru import logger
from flask import Blueprint, request
from sqlalchemy.orm import Session

from .handlers import format_response
from ...models import dto
from ...orm import SessionCtx, New
from ...exceptions import DataBaseException


new_bl = Blueprint('new', __name__)


def _get_new(session: Session, id: int) -> New:
    new: New | None = session.query(New).get(id)
    if new is None or new.deleted:
        raise DataBaseException(f'Объявление не найдено')
    return new


@new_bl.post('/create')
@format_response
def create_new():
    data = dto.NewCreateRequest.parse_obj(request.json)
    with SessionCtx() as session:
        new = New(
            body = data.body,
            user = request.headers['user-id']
        )
        session.add( new )
        session.commit()
        logger.success(f'Создана новость id={new.id}')
        
        return dto.NewResponse.from_orm(new)


@new_bl.get('/get')
@format_response
def get_new():
    with SessionCtx() as session:
        return [
            dto.NewResponse.from_orm(new)
            for new in session.query(New)
                .where(New.deleted == False)
                .order_by(New.id)
                .all()
        ]


@new_bl.post('/get-any')
@format_response
def get_any_new():
    with SessionCtx() as session:
        return [
            dto.NewResponse.from_orm(new)
            for new in session.query(New).all()
        ]


@new_bl.put('/edit')
@format_response
def edit_new():
    data = dto.NewUpdateRequest.parse_obj(request.json)
    with SessionCtx() as session:
        new = _get_new(session, data.id)
        new.body = data.body
        session.commit()
        logger.success(f'Изменена новость с id={new.id}')

        return dto.NewResponse.from_orm(new)


@new_bl.delete('/delete')
@format_response
def delete_new():
    data = dto.DeleteRequest.parse_obj(request.json)
    with SessionCtx() as session:
        new = _get_new(session, data.id)
        new.deleted = True
        session.commit()
        logger.success(f'Удалена новость с id={new.id}')

    return dto.SuccessResponse()
