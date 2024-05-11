from energy_gym_mainserver.orm import Base, engine, User, SessionCtx
from energy_gym_mainserver.models import UserRole


def start_base():
    try:
        print('Создание таблиц в БД...')
        Base.metadata.create_all(engine)
        with SessionCtx() as session:
            if session.query(User).where(User.role == UserRole.ADMIN).count == 0:
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
                session.commit()
    except Exception as e:
        print(f'Ошибка создания таблиц: {e}')
    else:
        print('Таблицы успешно созданы')

if __name__ == '__main__':
    start_base()
