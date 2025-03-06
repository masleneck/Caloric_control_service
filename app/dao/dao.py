from app.dao.base import BaseDAO
from app.models import User, Profile, Meal, FoodItem, MealFoodItem

from sqlalchemy.ext.asyncio import AsyncSession



class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_user_with_profile(cls, session: AsyncSession, user_data: dict) -> User:
        """
        Добавляет пользователя и привязанный к нему профиль.

        Аргументы:
        - session: AsyncSession - асинхронная сессия базы данных
        - user_data: dict - словарь с данными пользователя и профиля

        Возвращает:
        - User - объект пользователя
        """
        # Создаем пользователя из переданных данных
        user = cls.model(
            email=user_data['email'],
            username=user_data['username'],
            hashed_password=user_data['hashed_password']
        )
        session.add(user)
        await session.flush()  # Чтобы получить user.id для профиля

        # Создаем профиль, привязанный к пользователю
        profile = Profile(
            user_id=user.id,
            name=user_data['name'], # При использовании квадратных скобок Python ожидает, что ключ существует
            gender=user_data['gender'],
            weight=user_data['weight'],
            height=user_data['height'],
            goal=user_data['goal'],
            birthday_date=user_data.get('birthday_date'), # get() обрабатывает отсутствующие ключи, возвращая None или заданное значение по умолчанию
            activity_level=user_data['activity_level']
        )
        session.add(profile)

        # Один коммит для обеих операций
        await session.commit()

        return user  # Возвращаем объект пользователя


class ProfileDAO(BaseDAO):
    model = Profile


class MealDAO(BaseDAO):
    model = Meal


class FoodItemDAO(BaseDAO):
    model = FoodItem


class MealFoodItemDAO(BaseDAO):
    model = MealFoodItem
