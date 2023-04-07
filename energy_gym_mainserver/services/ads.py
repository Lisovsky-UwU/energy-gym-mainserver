from .abc import BaseService
from ..orm import Ads


class AdsDBService(BaseService[Ads]):
    ...
