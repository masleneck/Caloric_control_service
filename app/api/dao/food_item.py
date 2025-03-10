from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# from app.schemas.? import ?
from app.dao.base import BaseDAO
from app.models import FoodItem


class FoodItemDAO(BaseDAO):
    model = FoodItem

    @classmethod
    async def add_food_item(cls, session: AsyncSession, food_data: dict) -> int:
        '''
        Добавляет продукт в базу данных.
        
        : session: Асинхронная сессия базы данных.
        : food_data: Данные продукта (словарь).
        :return: ID добавленного продукта
        '''
        food = cls.model(**food_data)
        session.add(food)

        try:
            await session.flush()  # Позволяет получить ID перед коммитом
            logger.info(f'Продукт "{food.name}" добавлен в базу.')
            return food.id
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f'Ошибка при добавлении продукта: {e}')
            raise e
