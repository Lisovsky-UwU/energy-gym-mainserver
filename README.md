# Главный сервер "Энергия"

## Общее

Моя дипломная работа на бакалавр. Представляет из себя систему для спортивного зала "Энергия", который в свою очередь существует для студентов [ВУЗа СГУГиТ](https://sgugit.ru/) и который позволяет студентам тренироваться в нем, под наблюдением тренера.

Состоит из трех репозиториев:
- [Главный сервер](https://github.com/Lisovsky-UwU/energy-gym-mainserver) - содержит в себе всю основную логику работы;
- [Сервер авторизации](https://github.com/Lisovsky-UwU/energy-gym-mainserver) - в него приходят запросы, он определяет ограничения доступов и переадресует далее запросы в главный сервер;
- [Фронт](https://github.com/Lisovsky-UwU/energy-gym-front) - располагается на сервере авторизации и представляет из себя веб-фронт системы для студента и тренера.

Сервер авторизации и главный сервер должны использовать одну базу данных `PosgtreSQL 12+`. Система позволяет студентам записываться в спортивный зал, а тренеру отмечать посещаемость, которую после можно выгрузить в отчет Excel. Также тренер может создавать объявления для студентов, информируя их об изменениях в работе спортивного зала и иной информации. Зарегестрироваться в системе могут только студенты, чьи данные выгружены на сервер авторизации. 

Студенты могут записываться раз в месяц, 25 числа (настраиваемый параметр) на следующий месяц, на определенное время в рамках недели. Все это создается и работает автоматически. На основе созданных записей студентов, создаются отметки о посещаемости на месяц. Если студент пропускает 3 занятия (настраиваемый параметр) по неуважительной причине, то он блокируется и не сможет записаться на следующий месяц.

Также присутствует функционал администратора, который имеет полный доступ ко всем данным сервера и полный контроль над ними, однако отсутствует графический интерфейс для него.

## Описание главного сервера

Сам сервер не должен получать никакие запросы от пользователей, все запросы должны проходить через сервер авторизации, который уже переадресует их главному серверу. Написан на Flask, для общения с БД используется SQLAlchemy, для конфигурации сервера используется [Parametrica](https://github.com/FosterToster/parametrica), для логирования используется [Loguru](https://github.com/Delgan/loguru). Автоматически создает времена для записи студентов, их отметки и проверяет заблокированных сутдентов. 

Общение главного сервера и сервера авторизации осуществляется через токен, который генерирует главный сервер и который можно будет найти в файле `config.yaml`, создаваемом при первом запуске приложения, в группе параметров `common` под параметром `token`. Его следует занести в параметры сервера авторизации.

Для подключения к БД нужно настроить параметры в группе `database`, в конфигурационном файле `config.yaml`. После их настройки, следует запустить файл `create_db.py`, который создаст всю необходимую структуру таблиц в БД.
