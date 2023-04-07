from typing import List
from typing import Dict
from pydantic import BaseModel

from .common import AvailableTimeModel
from .common import EntryModel
from .common import UserModel
from .common import AdsModel


# ---> Common <---

class DeleteResult(BaseModel):
    result : Dict[int, str]


# ---> Ads <---

class AdsList(BaseModel):
    data : List[AdsModel]


# ---> Available Time <---

class AvailableTimeList(BaseModel):
    data : List[AvailableTimeModel]


# ---> Entries <---

class EntryList(BaseModel):
    data : List[EntryModel]


# ---> Users <---

class UserList(BaseModel):
    data : List[UserModel]
