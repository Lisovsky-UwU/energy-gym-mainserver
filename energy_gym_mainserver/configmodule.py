from uuid import uuid4

from .ext.parametrica import Field
from .ext.parametrica import Fieldset
from .ext.parametrica import Metaconfig
from .ext.parametrica.io import YAMLFileConfigIO


class CommonSettings(Fieldset):

    use_dev               = Field[bool](True).label('Использовать ли окружение разработки')
    token                 = Field[str](str(uuid4())).label('Токен для доступа к серверу')
    max_entry_count       = Field[int](3).label('Максимальное количество записей для одного пользователя')
    date_format           = Field[str]('%d.%m.%Y').label('Формат для даты')
    visit_manager_timeout = Field[int](60).label('Время сна для менеджера создания отметок')


class AvailableTimeSettings(Fieldset):

    month_format   = Field[str]('%m-%Y').label('Формат месяца для доступного времени записи в БД')
    day_create     = Field[int](20).label('В какой день будут создаваться доступное время на следующий месяц')
    persons_numb   = Field[int](12).label('Количество свободных мест в создаваемых временах')
    opening_time   = Field[str]('12:00:00 25').label('Время открытия записи в формате ЧЧ:ММ:СС ДД')


class LocalServerSettings(Fieldset):

    host    = Field[str]('0.0.0.0').label('Адрес')
    port    = Field[int](5010).label('Порт')
    threads = Field[int](4).label('Количество потоков сервера')

    @property
    def address(self):
        return f'{self.host}:{self.port}'


class DataBaseSettings(Fieldset):

    host      = Field[str]('127.0.0.1').label('Адрес')
    port      = Field[int](5432).label('Порт')
    user      = Field[str]('').label('Логин для доступа')
    password  = Field[str]('').label('Пароль для доступа')
    base_name = Field[str]('energy-gym').label('Название БД')
    engine    = Field[str]('psycopg2').label('Движок для работы sqlalchemy')

    @property
    def connection_string(self) -> str:
        return f'postgresql+{self.engine}://{self.user}:{self.password}@{self.host}:{self.port}/{self.base_name}'


class ReportSettings(Fieldset):

    format_day    = Field[str]('%d.%m').label('Формат даты в отчетах')
    mark_skip     = Field[str]('-').label('Отметка о пропкусе в отчете')
    mark_presence = Field[str]('+').label('Отметка о присутствии в отчете')
    mark_valid    = Field[str]('*').label('Отметка об уважительном пропуске в отчете')
    mark_canceled = Field[str]('#').label('Отметка при отмененном занятии')

    def get_for_mark(self, mark: int) -> str:
        if mark == 0:
            return self.mark_skip
        elif mark == 1:
            return self.mark_presence
        elif mark == 2:
            return self.mark_valid
        else:
            return self.mark_canceled


class LogSettings(Fieldset):

    level     = Field[str]('INFO').label('Уровень логирования').hint('CRITICAL, ERROR, SUCCESS, INFO, DEBUG, TRACE')
    retention = Field[int](10).label('Время хранения логов в днях')


class Config(Metaconfig):

    common          = Field[CommonSettings]().label('Общие настройки')
    available_time  = Field[AvailableTimeSettings]().label('Настройки доступного времени для записи')
    local_server    = Field[LocalServerSettings]().label('Настройки локального сервера')
    database        = Field[DataBaseSettings]().label('Настройки базы данных')
    report          = Field[ReportSettings]().label('Настройки отчетов')
    log             = Field[LogSettings]().label('Настройка логгирования')


config = Config(YAMLFileConfigIO('config.yaml'))
