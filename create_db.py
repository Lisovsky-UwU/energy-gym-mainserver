from energy_gym_mainserver.orm import Base, engine, User, SessionCtx
from energy_gym_mainserver.models import UserRole


def start_base():
    try:
        print('Создание БД...')
        Base.metadata.create_all(engine)
        print('Таблицы созданы')
        with SessionCtx() as session:
            print('Проверка существования админа по умолчанию')
            if session.query(User).where(User.role == UserRole.ADMIN and User.deleted == False).count() == 0:
                print('Админ по умолчанию отсутствует, создаем')
                session.add(
                    User(
                        student_card = -77712,
                        firstname    = 'SUPER',
                        secondname   = 'ADMIN',
                        surname      = '',
                        group        = '-',
                        hid          = '11b788fc93d1332d76460c77b8d4dd406f2f9f8ab6ef5c398df319a69664f0c5', # password: hexReGON14
                        role         = 'ADMIN',
                    )
                )
                print('Админ успешно создан (login=-77712, password=hexReGON14)')
                session.commit()
            else:
                print('Админ в БД уже существует')
    except Exception as e:
        print(f'Ошибка создания таблиц: {e}')
    else:
        print('БД успешно создана')

if __name__ == '__main__':
    start_base()
