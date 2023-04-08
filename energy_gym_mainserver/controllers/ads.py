from typing import Type
from typing import Iterable
from typing import Tuple
from typing import Dict
from datetime import datetime

from ..services import AdsDBService
from ..models import dto
from ..orm import Ads


class AdsDBController:

    def __init__(self, ads_service_type: Type[AdsDBService]):
        self.service_type = ads_service_type


    def create(self, user_id: int, payload: Iterable[str]) -> Tuple[dto.AdsModel]:
        with self.service_type() as service:
            result_list = service.create_for_iter(
                Ads(
                    create_time = datetime.now(),
                    body        = body,
                    user        = user_id,
                )
                for body in payload
            )
            service.commit()

            return self.__to_tuple_model__(result_list)


    def get_all(self, get_deleted: bool = False) -> Tuple[dto.AdsModel]:
        with self.service_type() as service:
            return self.__to_tuple_model__(service.get_all(get_deleted))
        
    
    def update(self, payload: Iterable[dto.AdsUpdateRequest]) -> dto.AdsModel:
        with self.service_type() as service:
            result_list = list()

            for data in payload:
                ads = service.get_by_id(data.id)
                if ads is None or ads.deleted:
                    continue

                ads.body = data.body
                service.update(ads)
                result_list.append(ads)

            service.commit()

            return self.__to_tuple_model__(result_list)
        

    def delete(self, id_list: Iterable[int]) -> Dict[int, str]:
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


    def __to_tuple_model__(self, data: Iterable[Ads]) -> Tuple[dto.AdsModel]:
        return tuple(
            dto.AdsModel.from_orm(ads_db)
            for ads_db in data
        )