from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# from app.schemas.? import ?
from app.dao.base import BaseDAO
from app.models import MealFoodItem


class MealFoodItemDAO(BaseDAO):
    model = MealFoodItem

    @classmethod
    async def add_food_to_meal(cls, session: AsyncSession, meal_id: int, food_item_id: int, quantity: float) -> None:
        '''
        Добавляет связь между приемом пищи и продуктом.

        :param session: Сессия базы данных.
        :param meal_id: ID приема пищи.
        :param food_item_id: ID продукта.
        :param quantity: Количество продукта (в граммах, например).
        '''
        meal_food_item = cls.model(meal_id=meal_id, food_item_id=food_item_id, quantity=quantity)
        session.add(meal_food_item)

        try:
            await session.commit()
            logger.info(f'Продукт "{food_item_id}" добавлен в прием пищи {meal_id}.')
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f'Ошибка при добавлении продукта в прием пищи: {e}')
            raise e

