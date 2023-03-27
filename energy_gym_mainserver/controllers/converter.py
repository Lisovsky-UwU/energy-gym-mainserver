from ..models.dto import AvailableTimeModel
from ..models.dto import EntryModel
from ..models.dto import UserModel
from ..orm import AvailableTime
from ..orm import Entry
from ..orm import User


class DTOConverter:

    def avtime_to_model(self, _from: AvailableTime, free_seats: int) -> AvailableTimeModel:
        res = AvailableTimeModel.from_orm(_from)
        res.free_seats = free_seats
        return res


    def entry_to_model(self, _from: Entry, selected_time: AvailableTimeModel, user: UserModel) -> EntryModel:
        res = EntryModel.from_orm(_from)
        res.selected_time = selected_time
        res.user = user
        return res
    

    def user_to_model(self, _from: User) -> UserModel:
        return UserModel.from_orm(_from)
