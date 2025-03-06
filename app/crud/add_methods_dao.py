# python -m app.crud.add_methods_dao

from typing import List
from datetime import datetime
from asyncio import run
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import UserDAO
from app.core.db import connection
from app.models.profiles import Gender, СurrentGoal, ActivityLevel

@connection
async def add_one(user_data: dict, session: AsyncSession):
    new_user = await UserDAO.add(session=session, **user_data)
    print(f"Добавлен новый пользователь с ID: {new_user.id}")
    return new_user.id

# one_user = {"email": "oliver.jackson@example.com", "username": "oliver_jackson", "hashed_password": "jackson123"}
# run(add_one(user_data=one_user))


@connection
async def add_many_users(users_data: List[dict], session: AsyncSession):
    new_users = await UserDAO.add_many(session=session, instances=users_data)
    user_ilds_list = [user.id for user in new_users]
    print(f"Добавлены новые пользователи с ID: {user_ilds_list}")
    return user_ilds_list

# users = [
#     {"email": "amelia.davis@example.com","username": "amelia_davis", "hashed_password": "davispassword"},
#     {"email": "lucas.white@example.com","username": "lucas_white", "hashed_password": "whiteSecure"},
#     {"email": "mia.moore@example.com","username": "mia_moore", "hashed_password": "moorepass098"},
#     {"email": "benjamin.hall@example.com","username": "benjamin_hall", "hashed_password": "hallben123"},
#     {"email": "sophia.hill@example.com","username": "sophia_hill", "hashed_password": "hillSophia999"},
#     {"email": "liam.green@example.com","username": "liam_green", "hashed_password": "greenSecure789"},
#     {"email": "isabella.clark@example.com","username": "isabella_clark", "hashed_password": "clarkIsabella001"},
#     {"email": "ethan.baker@example.com","username": "ethan_baker", "hashed_password": "bakerEthan555"},
#     {"email": "charlotte.scott@example.com","username": "charlotte_scott", "hashed_password": "scottcharl333"},
#     {"email": "logan.young@example.com","username": "logan_young", "hashed_password": "younglogan876"}
# ]

# run(add_many_users(users_data=users))


@connection
async def add_full_user(user_data: dict, session: AsyncSession):
    new_user = await UserDAO.add_user_with_profile(session=session, user_data=user_data)
    print(f"Добавлен новый пользователь с ID: {new_user.id}")
    return new_user.id

# user_data = {
#     "email": "QWEQWE@example.com",
#     "username": "QWEQWE",
#     "hashed_password": "QWEQWE123321",
#     "name": "Paul",
#     "gender": Gender.FEMALE,
#     "weight": 59.7,
#     "height": 155,
#     "goal": СurrentGoal.GAIN_MUSCLE_MASS,
#     "birthday_date": datetime(1990, 7, 15, 10, 45, 0),
#     "activity_level": ActivityLevel.SEDENTARY
#     }
   
# run(add_full_user(user_data=user_data))













#  {
#         "email": "smithman@example.com",
#         "username": "smithman",
#         "hashed_password": "smithman456",
#         "name": "Sarah",
#         "gender": Gender.FEMALE,
#         "weight": 58.7,
#         "height": 165,
#         "goal": СurrentGoal.GAIN_MUSCLE_MASS,
#         "birthday_date": datetime(1998, 7, 15, 11, 45, 0),
#         "activity_level": ActivityLevel.MODERATE
#     },
#     {
#         "email": "johnson@example.com",
#         "username": "johnson",
#         "hashed_password": "johnson789",
#         "name": "Michael",
#         "gender": Gender.MALE,
#         "weight": 72.3,
#         "height": 175,
#         "goal": СurrentGoal.LOSE_WEIGHT,
#         "birthday_date": datetime(2002, 12, 25, 16, 30, 0),
#         "activity_level": ActivityLevel.NOT_STATED
#     },
#     {
#         "email": "williams@example.com",
#         "username": "williams",
#         "hashed_password": "williams012",
#         "name": "Emma",
#         "gender": Gender.FEMALE,
#         "weight": 62.1,
#         "height": 168,
#         "goal": СurrentGoal.KEEPING_FIT,
#         "birthday_date": datetime(1999, 3, 20, 13, 15, 0),
#         "activity_level": ActivityLevel.ATHLETE
#     },
#     {
#         "email": "brown@example.com",
#         "username": "brown",
#         "hashed_password": "brown345",
#         "name": "David",
#         "gender": Gender.MALE,
#         "weight": 78.9,
#         "height": 178,
#         "goal": СurrentGoal.NOT_STATED,
#         "birthday_date": datetime(2000, 9, 10, 15, 20, 0),
#         "activity_level": ActivityLevel.SEDENTARY
#     }

