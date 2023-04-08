from uuid import uuid4

from .ext.parametrica import Field
from .ext.parametrica import Fieldset
from .ext.parametrica import Metaconfig
from .ext.parametrica.io import YAMLFileConfigIO


class CommonSettings(Fieldset):

    use_dev         = Field[bool](True).label('Использовать ли окружение разработки')
    token           = Field[str](str(uuid4())).label('Токен для доступа к серверу')
    max_entry_count = Field[int](3).label('Максимальное количество записей для одного пользователя')


class AvailableTimeSettings(Fieldset):

    month_format   = Field[str]('%m-%Y').label('Формат месяца для доступного времени записи в БД')
    day_create     = Field[int](20).label('В какой день будут создаваться доступное время на следующий месяц')
    persons_numb   = Field[int](12).label('Количество свободных мест в создаваемых временах')
    opening_time   = Field[str]('12:00:00 25').label('Время открытия записи в формате ЧЧ:ММ:СС ДД')


class LocalServerSettings(Fieldset):

    host = Field[str]('0.0.0.0').label('Адрес')
    port = Field[int](5010).label('Порт')

    @property
    def address(self):
        return f'{self.host}:{self.port}'


class DataBaseSettings(Fieldset):

    host      = Field[str]('127.0.0.1').label('Адрес')
    port      = Field[int](5432).label('Порт')
    user      = Field[str]('').label('Логин для доступа')
    password  = Field[str]('').label('Пароль для доступа')
    base_name = Field[str]('energy-gym').label('Название БД')

    @property
    def connection_string(self) -> str:
        return f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.base_name}'


class Config(Metaconfig):

    common          = Field[CommonSettings]().label('Общие настройки')
    available_time  = Field[AvailableTimeSettings]().label('Настройки доступного времени для записи')
    local_server    = Field[LocalServerSettings]().label('Настройки локального сервера')
    database        = Field[DataBaseSettings]().label('Настройки базы данных')


config = Config(YAMLFileConfigIO('config.yaml'))
