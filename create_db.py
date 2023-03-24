from sqlalchemy import text
from energy_gym_server.models.database import Base, engine, User
from energy_gym_server.models import UserRoles


def start_base():
    try:
        print('Создание таблиц в БД...')
        Base.metadata.create_all(engine)
        with engine.begin() as conn:
            conn.execute(
                text(f"INSERT INTO {User.__tablename__} VALUES (-1, 'ADMIN', '-', 'hexReGON14', '{UserRoles.ADMIN.name}')")
            )
    except Exception as e:
        print(f'Ошибка создания таблиц: {e}')
    else:
        print('Таблицы успешно созданы')

if __name__ == '__main__':
    start_base()
