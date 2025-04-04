

from fastapi import HTTPException
from app.models.food_items import FoodItems
from app.repositories.base import BaseDAO
from app.schemas.meals import FoodItemCreate


class FoodItemDAO(BaseDAO[FoodItems]):
    model = FoodItems
    
    async def create_food_item(self, food_data: FoodItemCreate) -> FoodItems:
        """Создает новый продукт"""
        # Проверяем, не существует ли уже продукт с таким названием
        existing_item = await self.find_one_by_fields(name=food_data.name)
        if existing_item:
            raise HTTPException(400,detail="Продукт с таким названием уже существует")
        
        new_item = self.model(**food_data.model_dump())
        self._session.add(new_item)
        await self._session.commit()
        return new_item