from .ext.parametrica import Field
from .ext.parametrica import Fieldset
from .ext.parametrica import Metaconfig
from .ext.parametrica.io import YAMLFileConfigIO


class CommonSettings(Fieldset):

    use_dev         = Field[bool](True).label('Использовать ли окружение разработки')
    av_month_format = Field[str]('%m-%Y').label('Формат месяца для доступного времени записи в БД')


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
    local_server    = Field[LocalServerSettings]().label('Настройки локального сервера')
    database        = Field[DataBaseSettings]().label('Настройки базы данных')


config = Config(YAMLFileConfigIO('config.yaml'))
