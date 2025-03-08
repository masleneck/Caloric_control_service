# python -m app.crud.select_methods_dao

from app.dao.dao import UserDAO
from app.core.db import connection
from app.schemas.users import UserPydantic, UsernameIdPydantic

from asyncio import run


@connection
async def select_all_users(session):
    return await UserDAO.get_all_users(session)

'''

all_users = run(select_all_users())
for i in all_users:
    user_pydantic = UserPydantic.from_orm(i)
    # Метод from_orm в Pydantic используется для создания экземпляра Pydantic модели на основе объекта ORM. 
    # Этот метод автоматически преобразует данные из ORM объекта в Pydantic модель, 
    # что позволяет легко работать с данными, извлеченными из базы данных через ORM (например, SQLAlchemy).
    print(user_pydantic.dict())

# То есть, когда мы выполним преобразование, мы получим новую модель Pydantic, которая будет основана на полученных данных с SQLAlchemy. 
# Это дает нам мощный инструмент для работы, так у объектов Pydantic-моделей много методов, в частности, методы, 
# которые трансформируют объект Pydantic модели в JSON или dict. print(user_pydantic) or print(user_pydantic.dict/json())

'''

@connection
async def select_username_id(session):
    return await UserDAO.get_username_id(session)
'''

# rez = run(select_username_id())
# for i in rez:
#     print(i)
# Результат мы получили уже в виде кортежей не именованных. 
# То есть, у нас сейчас нет возможности достать нужное значение по ключу и не сработает наш метод to_dict(),
# так как работает он только с объектом модели.

# Опишем новую Pydantic-схему, которая позволит корректно отобразить значения из эти последнего метода.
rez = run(select_username_id())
for i in rez:
    rez = UsernameIdPydantic.from_orm(i)
    print(rez.dict())

'''


@connection
async def select_full_user_info(session, user_id: int):
    rez = await UserDAO.find_one_or_none_by_id(session=session, data_id=user_id)
    if rez:
        return UserPydantic.from_orm(rez).dict()
    return {'message': f'Пользователь с ID {user_id} не найден!'}
# Здесь мы сразу преобразуем результат в питоновский словарь через Pydantic-схему.


# info = run(select_full_user_info(user_id=1))
# print(info)


# Попробуем найти пользователя по его электронной почте и ID, используя этот метод:
@connection
async def select_full_user_info_email(session, user_id: int, email: str):
    rez = await UserDAO.find_one_or_none(session=session, id=user_id, email=email)
    if rez:
        return UserPydantic.from_orm(rez).dict()
    return {'message': f'Пользователь с ID {user_id} не найден!'}


# info = run(select_full_user_info_email(user_id=1, email='example@example.com'))
# print(info)

