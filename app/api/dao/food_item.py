from sqlalchemy import select
from typing import Optional
from app.dao.base import BaseDAO
from app.models.food_items import FoodItem

class FoodItemDAO(BaseDAO[FoodItem]):
    model = FoodItem

    async def get_food_item_by_id(self, food_item_id: int) -> FoodItem | None:
        '''Получить продукт по ID с проверкой существования'''
        return await self.find_one_or_none_by_id(food_item_id)