from collections import defaultdict
from datetime import date
from sqlalchemy import and_, func, select, delete
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from app.models.food_items import FoodItems
from app.models.meal_food_items import MealFoodItem
from app.models.meals import Meals
from app.repositories.base import BaseDAO
from app.schemas.meals import DailyMealsResponse, DailyNutritionResponse, MealProductsResponse, MealUpsertRequest

class MealDAO(BaseDAO[Meals]):
    model = Meals

    async def upsert_meal_with_items(
        self,
        user_id: int,
        meal_data: MealUpsertRequest,
    ) -> Meals:
        """Метод для создания/обновления приема пищи с продуктами"""
        capitalized_names = [name.capitalize() for name in meal_data.food_names]
        if len(capitalized_names) != len(meal_data.food_quantities):
            raise HTTPException(400,detail="Количество продуктов и граммовок не совпадает")
        # Проверяем существование продуктов
        stmt = select(FoodItems).where(FoodItems.name.in_(capitalized_names))
        result = await self._session.execute(stmt)
        db_food_items = result.scalars().all()

        if len(db_food_items) != len(capitalized_names):
            found_names = {item.name for item in db_food_items}
            not_found = [
                name for name in capitalized_names 
                if name not in found_names
            ]
            raise HTTPException(404,detail=f"Продукты не найдены: {', '.join(not_found)}")
        # Ищем существующий прием пищи
        existing_meal = await self.find_one_by_fields(
            user_id=user_id,
            mealtime=meal_data.mealtime,
            meal_date=meal_data.meal_date
        )
        # Подготавливаем данные для связей
        name_to_item = {item.name: item for item in db_food_items}
        meal_food_items = [
            MealFoodItem(
                food_item_id=name_to_item[name].id,
                quantity=meal_data.food_quantities[i]
            )
            for i, name in enumerate(capitalized_names)
        ]
        # Создаем или обновляем прием пищи
        if existing_meal:
            # Удаляем старые связи
            await self._session.execute(
                delete(MealFoodItem).where(MealFoodItem.meal_id == existing_meal.id)
            )
            meal = existing_meal
        else:
            meal = Meals(
                mealtime=meal_data.mealtime,
                meal_date=meal_data.meal_date,
                user_id=user_id
            )
            self._session.add(meal)
        
        await self._session.flush()
        # Добавляем новые связи
        for mfi in meal_food_items:
            mfi.meal_id = meal.id
            self._session.add(mfi)

        await self._session.commit()
        return meal
    

    async def get_daily_nutrition(
        self,
        user_id: int,
        target_date: date
    ) -> DailyNutritionResponse:
        """Возвращает сумму калорий, белков, жиров и углеводов за указанный день"""
        # Запрос для агрегации данных
        stmt = select(
            func.coalesce(func.sum(FoodItems.calories * MealFoodItem.quantity / 100), 0).label("total_calories"),
            func.coalesce(func.sum(FoodItems.proteins * MealFoodItem.quantity / 100), 0).label("total_proteins"),
            func.coalesce(func.sum(FoodItems.fats * MealFoodItem.quantity / 100), 0).label("total_fats"),
            func.coalesce(func.sum(FoodItems.carbs * MealFoodItem.quantity / 100), 0).label("total_carbs")
        ).select_from(Meals)\
            .join(MealFoodItem, Meals.id == MealFoodItem.meal_id)\
            .join(FoodItems, MealFoodItem.food_item_id == FoodItems.id)\
            .where(
                and_(
                    Meals.user_id == user_id,
                    Meals.meal_date == target_date
                )
            )

        result = await self._session.execute(stmt)
        nutrition_data = result.mappings().one()
        
        return DailyNutritionResponse(**nutrition_data)
    

    async def get_daily_meals(
        self,
        user_id: int,
        target_date: date
    ) -> DailyMealsResponse:
        """ Получает все приемы пищи за день с продуктами"""
        stmt = (
            select(Meals, FoodItems, MealFoodItem.quantity)
            .join(MealFoodItem, Meals.id == MealFoodItem.meal_id)
            .join(FoodItems, MealFoodItem.food_item_id == FoodItems.id)
            .where(
                and_(
                    Meals.user_id == user_id,
                    Meals.meal_date == target_date
                )
            )
            .order_by(Meals.mealtime)
        )

        result = await self._session.execute(stmt)
        rows = result.all()

        # Группируем по приемам пищи
        meals_dict = defaultdict(list)
        for meal, food_item, quantity in rows:
            meals_dict[meal.mealtime].append(f"{food_item.name} ({quantity}g)")

        return DailyMealsResponse(
            date=target_date,
            meals={
                mealtime: MealProductsResponse(
                    mealtime=mealtime,
                    products=products
                )
                for mealtime, products in meals_dict.items()
            }
        )
    
