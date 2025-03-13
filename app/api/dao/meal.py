
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete as sqlalchemy_delete, select, update as sqlalchemy_update, cast, Date, and_
from datetime import datetime, date
from typing import List
from app.dao.base import BaseDAO
from app.models import Meal, Mealtime, MealFoodItem
from app.schemas.meals import MealCreate, MealDetailResponse, MealFoodItemResponse, FoodItemShortResponse
from .meal_food_item import MealFoodItemDAO
from app.core.exceptions import InvalidMealData

class MealDAO(BaseDAO[Meal]):
    model = Meal
    
    async def create_meal(self, user_id: int, food_item_id: int, mealtime: Mealtime, meal_date: datetime, quantity: float) -> int:
        try:
            # Создаем сам прием пищи
            meal = Meal(
                user_id=user_id,
                mealtime=mealtime,
                meal_date=meal_date
            )
            self._session.add(meal)
            await self._session.flush()

            # Добавляем продукт
            await MealFoodItemDAO(self._session).add_food_to_meal(
                meal_id=meal.id,
                food_item_id=food_item_id,
                quantity=quantity
            )
            return meal.id
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise InvalidMealData(detail=str(e))


    async def get_meal_by_id(
        self,
        meal_id: int,
    ) -> Meal | None:
        return await self.find_one_or_none_by_id(meal_id)
    

    async def delete_meal(self, meal_id: int) -> None:
        '''Удаляет приём пищи и все связанные записи.'''
        await self._session.execute(
            sqlalchemy_delete(Meal).where(Meal.id == meal_id)
        )
        await self._session.flush()


    async def get_meals_by_date(
        self, 
        user_id: int, 
        target_date: date  
    ) -> List[MealDetailResponse]:
        query = (
            select(Meal)
            .options(
                joinedload(Meal.meal_food_links)
                .joinedload(MealFoodItem.food_item)
            )
            .where(
                and_(
                    Meal.user_id == user_id,
                    cast(Meal.meal_date, Date) == target_date  
                )
            )
        )
        result = await self._session.execute(query)
        meals = result.unique().scalars().all()
        return [
            MealDetailResponse(
                id=meal.id,
                mealtime=meal.mealtime,
                meal_date=meal.meal_date,
                total_calories=sum(
                    link.quantity * link.food_item.calories / 100
                    for link in meal.meal_food_links
                ),
                food_items=[
                    MealFoodItemResponse(
                        id=link.id,
                        meal_id=link.meal_id,
                        food_item=FoodItemShortResponse(
                            id=link.food_item.id,
                            name=link.food_item.name,
                            calories=link.food_item.calories,
                            proteins=link.food_item.proteins,
                            fats=link.food_item.fats,
                            carbs=link.food_item.carbs
                        ),
                        quantity=link.quantity
                    )
                    for link in meal.meal_food_links
                ]
            )
            for meal in meals
        ]


    async def update_meal(
        self,
        meal_id: int,
        mealtime: Mealtime | None = None,
        meal_date: datetime | None = None,
    ) -> None:
        '''Обновляет приём пищи.'''
        update_data = {}
        if mealtime:
            update_data['mealtime'] = mealtime
        if meal_date:
            update_data['meal_date'] = meal_date

        if update_data:
            await self._session.execute(
                sqlalchemy_update(Meal)
                .where(Meal.id == meal_id)
                .values(**update_data)
            )
            await self._session.flush()