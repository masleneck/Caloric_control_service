

from typing import List
from fastapi import HTTPException
from sqlalchemy import func, or_, select
from app.models.food_items import FoodItem
from app.repositories.base import BaseDAO
from app.schemas.meals import FoodItemCreate, FoodItemResponse


class FoodItemDAO(BaseDAO[FoodItem]):
    model = FoodItem

    async def search_foods(
        self,
        query: str,
        limit: int = 10,
        threshold: float = 0.3
    ) -> List[FoodItemResponse]:
        """
        поиск продуктов с комбинацией методов:
        - Сначала точное совпадение (регистронезависимое)
        - Затем триграммный поиск (pg_trgm) для нечеткого соответствия
        - В конце простой LIKE для остальных случаев
        -- !!! Включите расширение для триграммного поиска (если еще не включено)
        CREATE EXTENSION IF NOT EXISTS pg_trgm;
        :param query: Строка поиска (минимум 2 символа)
        :param limit: Максимальное количество результатов
        :param threshold: Порог схожести для триграммного поиска (0-1)
        """
        if len(query) < 2:
            raise HTTPException(400, detail="Поисковый запрос должен содержать минимум 2 символа")
        
        search = f"%{query}%"
        
        # Комбинированный запрос
        stmt = (
            select(self.model)
            .where(
                or_(
                    func.lower(self.model.name) == func.lower(query),  # Точное совпадение
                    func.similarity(self.model.name, query) > threshold,  # Триграммный поиск
                    self.model.name.ilike(search)  # Простой поиск по подстроке
                )
            )
            .order_by(
                func.lower(self.model.name) == func.lower(query).desc(),  # Точные совпадения выше
                func.similarity(self.model.name, query).desc(),  # Сортировка по схожести
                self.model.name  # Альфавитный порядок для остальных
            )
            .limit(limit)
        )
        
        result = await self._session.execute(stmt)
        foods = result.scalars().all()
        if not foods:
            raise HTTPException(404, detail="Продукты не найдены")
        
        return [FoodItemResponse.model_validate(food) for food in foods]



    async def create_food_item(self, food_data: FoodItemCreate) -> FoodItem:
        """Создает новый продукт"""
        # Проверяем, не существует ли уже продукт с таким названием
        capitalized_name = food_data.name.capitalize()
        existing_item = await self.find_one_by_fields(name=capitalized_name)
        if existing_item:
            raise HTTPException(400,detail="Продукт с таким названием уже существует")
        # Подготавливаем данные
        food_data_dict = food_data.model_dump()
        food_data_dict['name'] = capitalized_name
        
        new_item = await self.add(FoodItemCreate(**food_data_dict))

        await self._session.commit()
        return new_item
