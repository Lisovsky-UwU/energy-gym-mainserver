from loguru import logger
from flask import Blueprint, request
from sqlalchemy import and_

from .handlers import format_response
from ...orm import AvailableTime, SessionCtx
from ...utils import get_next_month
from ...models import dto


avtime_bl = Blueprint('avtime', __name__)


@avtime_bl.post('/create')
@format_response
def create_avtime():
    data = dto.AvailableTimeAddRequest.parse_obj(request.json)
    with SessionCtx() as session:
        avtime = AvailableTime(
            weekday = data.weekday,
            time = data.time,
            number_of_persons = data.numberOfPersons,
            month = data.month,
        )
        session.add(avtime)
        session.commit()
        logger.success(f'Создано время для записи с id={avtime.id}')

        return dto.AvailableTimeResponse.from_orm(avtime, calculate_available=False)


@avtime_bl.get('/get')
@format_response
def get_avtimes():
    with SessionCtx() as session:
        return [
            dto.AvailableTimeResponse.from_orm(avtime)
            for avtime in session.query(AvailableTime)
                .where(
                    and_(
                        AvailableTime.deleted == False,
                        AvailableTime.month == get_next_month()
                    )
                )
                .all()
        ]


@avtime_bl.post('/get-any')
@format_response
def get_any_avtimes():
    with SessionCtx() as session:
        return [
            dto.AvailableTimeAnyResponse.from_orm(avtime)
            for avtime in session.query(AvailableTime).all()
        ]


@avtime_bl.put('/edit')
@format_response
def edit_avtime():
    return dto.InDevelopResponse()


@avtime_bl.delete('/delete')
@format_response
def delete_avtime():
    return dto.InDevelopResponse()
