from loguru import logger
from flask import Blueprint, request
from sqlalchemy import and_
from datetime import datetime

from .handlers import format_response
from ...orm import Visit, SessionCtx, AvailableTime, Entry
from ...models import dto
from ...exceptions import DataBaseException


visit_bl = Blueprint('visit', 'visit')


@visit_bl.post('/get')
@format_response
def get_visit():
    data = dto.VisitGetReqeust.parse_obj( request.json )
    _filter = True

    if data.date is not None:
        _filter = and_(_filter, Visit.date == data.date)
    
    if data.time is not None:
        _filter = and_(_filter, AvailableTime.time == data.time)

    if data.month is not None:
        _filter = and_(_filter, AvailableTime.month == data.month)

    with SessionCtx() as session:
        return [
            dto.GetVisitResponse.from_orm(visit)
            for visit in session.query(Visit).where(_filter).join(Visit.entry_model).join(Entry.available_time).all()
        ]


@visit_bl.put('/edit')
@format_response
def edit_visits():
    data = dto.VisitUpdateRequest.parse_obj( request.json )

    with SessionCtx() as session:
        visit: Visit | None = session.query(Visit).get(data.id)
        if visit is None:
            raise DataBaseException(f'Отметка посещения с id={data.id} не найдена')

        visit.mark = data.mark
        session.commit()
        
        logger.success(f'Изменена отметка посещения id={data.id} на mark={visit.mark}')
        return dto.GetVisitResponse.from_orm(visit)


@visit_bl.post('/cancel-lesson')
@format_response
def cancle_lesson():
    data = dto.CancelLessonRequest.parse_obj( request.json )

    with SessionCtx() as session:
        visits = (
            session.query(Visit)
                .join(Visit.entry_model)
                .join(Entry.available_time)
                .where(
                    and_(
                        Visit.deleted == False,
                        Visit.date == data.date,
                        AvailableTime.time == data.time
                    )
                )
                .all()
        )
        for visit in visits:
            visit.mark = 3
        
        session.commit()
        logger.success(f'Занятие на {data.date} в {data.time} отменено')

        return dto.SuccessResponse()
