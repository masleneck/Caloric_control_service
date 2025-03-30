# from datetime import date
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.data.repository.meal import MealDAO
# from app.dependencies.database_dep import get_session_with_commit
# from app.dependencies.auth_dep import get_current_user
# from app.schemas.meals import MealProductsResponse, Mealtime, MealUpdateRequest, NutritionalInfo, BaseMeal
# from app.models.users import User
# from app.core.exceptions import MealNotFound, NutritionalInfoNotFound, FoodItemNotFound, InvalidQuantity

# router = APIRouter(
#     prefix='/meals',
#     tags=['Приёмы пищи 🍽']
# )

# @router.get('/info/{meal_date}', response_model=NutritionalInfo, summary='Получить информацию о питании за день')
# async def get_nutritional_info(
#     meal_date: date,
#     session: AsyncSession = Depends(get_session_with_commit),
#     current_user: User = Depends(get_current_user)
# ):
#     '''Получить информацию о питании за день.'''
#     dao = MealDAO(session)
#     try:
#         nutritional_info = await dao.get_nutritional_info(
#             user_id=current_user.id,
#             meal_date=meal_date
#         )
#         return nutritional_info
#     except NutritionalInfoNotFound as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

# @router.get('/{meal_date}/{mealtime}', response_model=MealProductsResponse, summary='Получить прием пищи по дате')
# async def get_meal_by_date_and_type(
#     meal_date: date,
#     mealtime: Mealtime,
#     session: AsyncSession = Depends(get_session_with_commit),
#     current_user: User = Depends(get_current_user)
# ):
#     '''Получить прием пищи по дате и типу.'''
#     dao = MealDAO(session)
#     try:
#         meal = await dao.get_meal_by_user_and_date(
#             user_id=current_user.id,
#             meal_date=meal_date,
#             mealtime=mealtime
#         )
#         return meal
#     except MealNotFound as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

# @router.put('/{meal_id}', response_model=BaseMeal, summary='Обновить или создать прием пищи')
# async def update_meal(
#     meal_id: int,
#     meal_data: MealUpdateRequest,
#     session: AsyncSession = Depends(get_session_with_commit),
#     current_user: User = Depends(get_current_user)
# ):
#     '''Обновить или создать прием пищи.'''
#     dao = MealDAO(session)
#     try:
#         meal = await dao.update_meal_with_food_items(
#             meal_id=meal_id,
#             meal_data=meal_data,
#             user_id=current_user.id
#         )
#         return meal
#     except (MealNotFound, FoodItemNotFound, InvalidQuantity) as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)