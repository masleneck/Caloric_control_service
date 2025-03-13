from sqlalchemy import delete as sqlalchemy_delete, select
from typing import List
from app.dao.base import BaseDAO
from app.models.meal_food_items import MealFoodItem
from app.schemas.meals import MealFoodItemResponse
from app.core.exceptions import InvalidMealData


class MealFoodItemDAO(BaseDAO[MealFoodItem]):
    model = MealFoodItem

    async def add_food_to_meal(self, meal_id: int, food_item_id: int, quantity: float):
        # Проверка на существование связи
        existing = await self.find_one_by_fields(
            meal_id=meal_id,
            food_item_id=food_item_id
        )
        if existing:
            raise InvalidMealData(detail='Продукт уже добавлен')
        
        # Создаем новую связь
        new_item = MealFoodItem(
            meal_id=meal_id,
            food_item_id=food_item_id,
            quantity=quantity
        )
        self._session.add(new_item)
        await self._session.flush()


    async def remove_food_from_meal(
        self,
        meal_id: int,
        food_item_id: int,
    ) -> None:
        '''Удаляет продукт из приёма пищи.'''
        await self._session.execute(
            sqlalchemy_delete(MealFoodItem)
            .where(MealFoodItem.meal_id == meal_id)
            .where(MealFoodItem.food_item_id == food_item_id)
        )
        await self._session.flush()



    async def get_food_items_by_meal(
        self,
        meal_id: int,
    ) -> List[MealFoodItemResponse]:
        '''Возвращает список продуктов для приёма пищи.'''
        result = await self._session.execute(
            select(MealFoodItem)
            .where(MealFoodItem.meal_id == meal_id)
        )
        food_items = result.scalars().all()
        return [
            MealFoodItemResponse(
                id=item.id,
                meal_id=item.meal_id,
                food_item_id=item.food_item_id,
                quantity=item.quantity,
            )
            for item in food_items
        ]