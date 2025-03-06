
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import run

from app.core.db import connection
from app.models import User, Profile

from app.models.profiles import Gender,СurrentGoal,ActivityLevel
from datetime import datetime

@connection
async def create_user_example_1(email: str, username: str, hashed_password: str, session: AsyncSession) -> int:
    """
    Создает нового пользователя с использованием ORM SQLAlchemy.

    Аргументы:
    - email: str - имя пользователя
    - username: str - адрес электронной почты
    - hashed_password: str - хеш пароля пользователя
    - session: AsyncSession - асинхронная сессия базы данных

    Возвращает:
    - int - идентификатор созданного пользователя
    """
    
    user = User(email=email, username=username, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    return user.id

# new_user_id = run(create_user_example_1(email="bobatea@example.com",
#                                         username="bobatea",
#                                         hashed_password="bobateabobatea"))

# print(f"Новый пользователь с идентификатором {new_user_id} создан")

@connection
async def get_user_by_id_example_2(email: str, username: str, hashed_password: str,
                                   name: str,
                                   gender: Gender,
                                   weight: float,
                                   height: int,
                                   goal: СurrentGoal,
                                   birthday_date: datetime | None,
                                   activity_level: ActivityLevel,
                                   session: AsyncSession) -> dict[str, int]:
    user = User(email=email, username=username, hashed_password=hashed_password)
    session.add(user)
    await session.commit()

    profile = Profile(
        user_id=user.id,
        name=name,
        gender=gender,
        weight=weight,
        height=height,
        goal=goal,
        birthday_date=birthday_date,
        activity_level=activity_level)

    session.add(profile)
    await session.commit()
    print(f'Создан пользователь с ID {user.id} и ему присвоен профиль с ID {profile.id}')
    return {'user_id': user.id, 'profile_id': profile.id}

@connection
async def get_user_by_id_example_3(email: str, username: str, hashed_password: str,
                                   name: str,
                                   gender: Gender,
                                   weight: float,
                                   height: int,
                                   goal: СurrentGoal,
                                   birthday_date: datetime | None,
                                   activity_level: ActivityLevel,
                                   session: AsyncSession) -> dict[str, int]:
    try:
        user = User(email=email, username=username, hashed_password=hashed_password)
        session.add(user)
        await session.flush()  # Промежуточный шаг для получения user.id без коммита

        profile = Profile(
            user_id=user.id,
            name=name,
            gender=gender,
            weight=weight,
            height=height,
            goal=goal,
            birthday_date=birthday_date,
            activity_level=activity_level)
        
        session.add(profile)

        # Один коммит для обоих действий
        await session.commit()

        print(f'Создан пользователь с ID {user.id} и ему присвоен профиль с ID {profile.id}')
        return {'user_id': user.id, 'profile_id': profile.id}

    except Exception as e:
        await session.rollback()  # Откатываем транзакцию при ошибке
        raise e


# user_profile = run(get_user_by_id_example_3(
#     email="cofeeman@example.com",
#     username="cofeeman",
#     hashed_password="cofeeman322",
#     name="Jane",
#     gender=Gender.FEMALE,
#     weight=55.5,
#     height=160,
#     goal=СurrentGoal.KEEPING_FIT,
#     birthday_date=datetime(2001, 4, 1, 14, 6, 0),
#     activity_level=ActivityLevel.ACTIVE
# ))



# Для массового добавления данных в SQLAlchemy существует удобный метод add_all. 
# Он работает аналогично методу add, но принимает на вход список экземпляров (инстансов). 
# С его помощью мы можем добавить сразу несколько записей за одну операцию. Давайте рассмотрим пример, 
# где добавим пять пользователей с использованием этого метода.

@connection
async def create_user_example_4(users_data: list[dict], session: AsyncSession) -> list[int]:
    """
    Создает нескольких пользователей с использованием ORM SQLAlchemy.

    Аргументы:
    - users_data: list[dict] - список словарей, содержащих данные пользователей
      Каждый словарь должен содержать ключи: 'email', 'username', 'hashed_password'.
    - session: AsyncSession - асинхронная сессия базы данных

    Возвращает:
    - list[int] - список идентификаторов созданных пользователей
    """
    users_list = [
        User(
            email=user_data['email'],
            username=user_data['username'],
            hashed_password=user_data['hashed_password']
        )
        for user_data in users_data
    ]
    session.add_all(users_list)
    await session.commit()
    return [user.id for user in users_list]

users = [
    {
        "email": "cofeem1an@example.com",
        "username": "cofeema2n",
        "hashed_password": "cofeema2n322",
    },
    {
        "email": "smithman@example.com",
        "username": "smithman",
        "hashed_password": "smithman456",
    },
    {
        "email": "johnson@example.com",
        "username": "johnson",
        "hashed_password": "johnson789",
    },
    {
        "email": "williams@example.com",
        "username": "williams",
        "hashed_password": "williams012",
    },
    {
        "email": "brown@example.com",
        "username": "brown",
        "hashed_password": "brown345",
    }
]


run(create_user_example_4(users_data=users))
