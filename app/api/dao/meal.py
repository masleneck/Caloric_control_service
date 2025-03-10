from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# from app.schemas.? import ?
from app.dao.base import BaseDAO
from app.models.meals import Meal, Mealtime


class MealDAO(BaseDAO):
    model = Meal

    @classmethod
    async def add_meal(cls, session: AsyncSession, user_id: int, mealtime: Mealtime, meal_date: str) -> int:
        '''
        Добавляет прием пищи.

        :param session: Сессия базы данных.
        :param user_id: ID пользователя.
        :param mealtime: Тип приема пищи.
        :param meal_date: Дата приема пищи в формате 'YYYY-MM-DD HH:MM:SS'.
        :return: ID приема пищи.
        '''
        meal = cls.model(user_id=user_id, mealtime=mealtime, meal_date=meal_date)
        session.add(meal)

        try:
            await session.flush()
            logger.info(f'Прием пищи "{mealtime.value}" добавлен для пользователя {user_id}.')
            return meal.id
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f'Ошибка при добавлении приема пищи: {e}')
            raise e

    @classmethod
    async def get_meals_by_user_id(cls, session: AsyncSession, user_id: int) -> list[Meal]:
        '''
        Получает все приемы пищи пользователя.

        :param session: Сессия базы данных.
        :param user_id: ID пользователя.
        :return: Список объектов Meal.
        '''
        stmt = select(cls.model).filter_by(user_id=user_id).order_by(cls.model.meal_date.desc())
        result = await session.execute(stmt)
        return result.scalars().all()
