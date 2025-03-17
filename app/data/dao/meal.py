from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload
from app.models.meals import Meal
from app.models.meal_food_items import MealFoodItem
from app.models.food_items import FoodItem
from app.data.dao import BaseDAO
from datetime import date
from app.schemas.meals import MealProductsResponse, NutritionalInfo, BaseMeal, MealUpdateRequest
from app.models import Mealtime
from app.core.exceptions import MealNotFound, InvalidQuantity, FoodItemNotFound, MealAlreadyExists



class MealDAO(BaseDAO[Meal]):
    model = Meal

    async def get_nutritional_info(
        self, user_id: int, meal_date: date
    ) -> NutritionalInfo:
        '''
        Получить информацию о питании за день.
    
        Args:
            user_id (int): ID пользователя.
            meal_date (date): Дата приема пищи.
    
        Returns:
            NutritionalInfo: Суммарные данные о питании за день.
    
        Raises:
            NutritionalInfoNotFound: Если данные о питании не найдены.
        '''
        query = (
            select(
                func.sum(FoodItem.calories * MealFoodItem.quantity / 100).label('calories'),
                func.sum(FoodItem.proteins * MealFoodItem.quantity / 100).label('proteins'),
                func.sum(FoodItem.fats * MealFoodItem.quantity / 100).label('fats'),
                func.sum(FoodItem.carbs * MealFoodItem.quantity / 100).label('carbs')
            )
            .select_from(Meal)  # Явно указываем таблицу meals
            .join(MealFoodItem, Meal.id == MealFoodItem.meal_id)
            .join(FoodItem, MealFoodItem.food_item_id == FoodItem.id)
            .where(Meal.user_id == user_id)
            .where(Meal.meal_date == meal_date)
        )
        result = await self._session.execute(query)
        nutritional_info = result.first()

        # Если данные не найдены, возвращаем нулевые значения
        if not nutritional_info or all(v is None for v in nutritional_info):
            return NutritionalInfo(
                calories=0,
                proteins=0,
                fats=0,
                carbs=0
            )

        return NutritionalInfo(**nutritional_info._asdict())
    
    


    async def get_meal_by_user_and_date(
        self, user_id: int, meal_date: date, mealtime: Mealtime
    ) -> MealProductsResponse:
        '''
        Получить прием пищи по дате и типу.
        
        Args:
            user_id (int): ID пользователя.
            meal_date (date): Дата приема пищи.
            mealtime (Mealtime): Тип приема пищи (breakfast, lunch, dinner).
        
        Returns:
            MealProductsResponse: mealtime и список имен продуктов.
        
        Raises:
            MealNotFound: Если прием пищи не найден.
        '''
        query = (
            select(Meal)
            .where(Meal.user_id == user_id)
            .where(Meal.meal_date == meal_date)
            .where(Meal.mealtime == mealtime)
            .options(selectinload(Meal.meal_food_links).selectinload(MealFoodItem.food_item))  # Загружаем связанные данные
        )
        result = await self._session.execute(query)
        meal = result.scalar_one_or_none()

        if not meal:
            raise MealNotFound(detail='Прием пищи не найден')

        # Получаем список имен продуктов
        products = [link.food_item.name for link in meal.meal_food_links]

        return MealProductsResponse(
            meal_id=meal.id,
            mealtime=meal.mealtime,
            products=products
        )




    async def update_meal_with_food_items(
        self, meal_id: int, meal_data: MealUpdateRequest, user_id: int
    ) -> BaseMeal:
        '''Обновить или создать прием пищи.
        
        Args:
            meal_id (int): ID приема пищи.
            meal_data (MealUpdateRequest): Данные для обновления.
            user_id (int): ID пользователя.
        
        Returns:
            BaseMeal: Обновленный или созданный прием пищи.
        
        Raises:
            MealNotFound: Если прием пищи не найден и не может быть создан.
            FoodItemNotFound: Если продукт не найден.
            InvalidQuantity: Если количество продукта недопустимо.
        '''
        # Проверяем, что количество продуктов и их названий совпадает
        if len(meal_data.names) != len(meal_data.quantities):
            raise InvalidQuantity(detail='Количество продуктов и их количеств должно совпадать')

        # Проверяем, что все количества больше 0
        # if any(q <= 0 for q in meal_data.quantities):
        #     raise InvalidQuantity(detail='Количество продукта должно быть больше 0')

         # Проверяем, что в этот день у пользователя нет другого приема пищи с таким же mealtime
        existing_meal = await self._session.execute(
            select(Meal)
            .where(Meal.user_id == user_id)
            .where(Meal.meal_date == meal_data.meal_date)
            .where(Meal.mealtime == meal_data.mealtime)
            .where(Meal.id != meal_id)  # Исключаем текущий прием пищи из проверки
        )
        existing_meal = existing_meal.scalar_one_or_none()

        if existing_meal:
            raise MealAlreadyExists(detail=f'Прием пищи ({meal_data.mealtime}) уже существует в этот день')
    
        # Находим или создаем прием пищи
        meal = await self.find_one_or_none_by_id(meal_id)
        if not meal:
            meal = Meal(
                id=meal_id,
                user_id=user_id,
                mealtime=meal_data.mealtime,
                meal_date=meal_data.meal_date
            )
            self._session.add(meal)
            await self._session.flush()

        # Проверяем, принадлежит ли прием пищи текущему пользователю
        if meal.user_id != user_id:
            raise MealNotFound(detail='Прием пищи не принадлежит текущему пользователю')

        # Удаляем старые связи
        await self._session.execute(
            delete(MealFoodItem).where(MealFoodItem.meal_id == meal_id)
        )

        # Находим продукты по их именам
        food_items = []
        for name in meal_data.names:
            query = select(FoodItem).where(FoodItem.name == name.capitalize())
            result = await self._session.execute(query)
            food_item = result.scalar_one_or_none()
            if not food_item:
                raise FoodItemNotFound(detail=f'Продукт "{name}" не найден')
            food_items.append(food_item)

        # Добавляем новые связи
        for food_item, quantity in zip(food_items, meal_data.quantities):
            meal_food_item = MealFoodItem(
                meal_id=meal_id,
                food_item_id=food_item.id,
                quantity=quantity
            )
            self._session.add(meal_food_item)

        await self._session.flush()
        await self._session.refresh(meal, ['meal_food_links'])
        return BaseMeal(**meal.to_pydantic())