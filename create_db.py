from energy_gym_mainserver.orm import Base
from energy_gym_mainserver.orm import engine
from energy_gym_mainserver.orm import User
from energy_gym_mainserver.models import UserRole
from energy_gym_mainserver.services import UserDBService


def start_base():
    try:
        print('Создание таблиц в БД...')
        Base.metadata.create_all(engine)
        with UserDBService() as service:
            service.create(
                User(
                    student_card = -1,
                    name         = 'ADMIN',
                    group        = '-',
                    password     = 'hexReGON14',
                    role         = UserRole.ADMIN.name,
                )
            )
    except Exception as e:
        print(f'Ошибка создания таблиц: {e}')
    else:
        print('Таблицы успешно созданы')

if __name__ == '__main__':
    start_base()
