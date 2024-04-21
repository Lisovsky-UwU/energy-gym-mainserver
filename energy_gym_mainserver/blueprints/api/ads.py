from typing import Union
from loguru import logger
from flask import Blueprint, request
from sqlalchemy.orm import Session

from .handlers import format_response
from ...models import dto
from ...orm import SessionCtx, Ads
from ...exceptions import DataBaseException


ads_bl = Blueprint('ads', __name__)


def _get_ads(session: Session, id: int) -> Union[Ads, None]:
    ads: Ads | None = session.query(Ads).where(Ads.deleted == False).get(id)
    if ads is None:
        raise DataBaseException(f'Объявление не найдено')
    return ads


@ads_bl.post('/create')
@format_response
def create_ads():
    data = dto.AdsCreateRequest.parse_obj(request.json)
    with SessionCtx() as session:
        ads = Ads(
            body = data.body,
            user = request.headers['user-id']
        )
        session.add( ads )
        session.commit()
        logger.success(f'Создано объявление id={ads.id}')
        
        return dto.AdsResponse.from_orm(ads)


@ads_bl.get('/get')
@format_response
def get_ads():
    with SessionCtx() as session:
        return [
            dto.AdsResponse.from_orm(ads)
            for ads in session.query(Ads)
                .where(Ads.deleted == False)
                .order_by(Ads.id)
                .all()
        ]


@ads_bl.post('/get-any')
@format_response
def get_any_ads():
    with SessionCtx() as session:
        return [
            dto.AdsResponse.from_orm(ads)
            for ads in session.query(Ads).all()
        ]


@ads_bl.put('/edit')
@format_response
def edit_ads():
    data = dto.AdsUpdateRequest.parse_obj(request.json)
    with SessionCtx() as session:
        ads = _get_ads(session, data.id)
        ads.body = data.body
        session.commit()
        logger.success(f'Изменено объявление с id={ads.id}')

        return dto.AdsResponse.from_orm(ads)


@ads_bl.delete('/delete')
@format_response
def delete_ads():
    data = dto.DeleteRequest.parse_obj(request.json)
    with SessionCtx() as session:
        ads = _get_ads(session, data.id)
        ads.deleted = True
        session.commit()
        logger.success(f'Удалено объявление с id={ads.id}')

    return dto.SuccessResponse()
