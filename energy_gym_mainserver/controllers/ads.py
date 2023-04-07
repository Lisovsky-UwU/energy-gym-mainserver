from typing import Type
from typing import List
from typing import Tuple
from typing import Dict
from datetime import datetime

from ..exceptions import LogicError
from ..services import AdsDBService
from ..models import dto
from ..orm import Ads


class AdsDBController:

    def __init__(self, ads_service_type: Type[AdsDBService]):
        self.service_type = ads_service_type


    def create(self, user_id: int, body: str) -> dto.AdsModel:
        with self.service_type() as service:
            ads = service.create(
                Ads(
                    create_time = datetime.now(),
                    body        = body,
                    user        = user_id,
                )
            )
            service.commit()

            return dto.AdsModel.from_orm(ads)


    def get_all(self, get_deleted: bool = False) -> Tuple[dto.AdsModel]:
        with self.service_type() as service:
            return tuple(
                dto.AdsModel.from_orm(ads_db)
                for ads_db in service.get_all(get_deleted)
            )
        
    
    def update(self, data: dto.AdsUpdateRequest) -> dto.AdsModel:
        with self.service_type() as service:
            ads = service.get_by_id(data.id)
            if ads is None:
                raise LogicError('Запрашиваемое объявление не найдено')

            ads.body = data.body
            service.update(ads)
            service.commit()

            return dto.AdsModel.from_orm(ads)
        

    def delete_for_id_list(self, id_list: List[int]) -> Dict[int, str]:
        with self.service_type() as service:
            result_dict = dict()

            for ads_id in id_list:
                ads = service.get_by_id(ads_id)

                if ads is None or ads.deleted:
                    result_dict[ads_id] = 'Запрашиваемое объявление не найдено'

                else:            
                    service.delete(ads)
                    result_dict[ads_id] = 'Успешно'

            service.commit()

            return result_dict
