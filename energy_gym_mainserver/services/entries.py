from .abc import BaseService
from ..orm import Entry


class EntriesService(BaseService[Entry]):
    ...
