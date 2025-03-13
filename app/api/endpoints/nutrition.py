from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
from typing import List
from loguru import logger
from app.models import User, Meal, Mealtime
from app.dependencies.auth_dep import get_current_user
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.schemas.meals import MealCreate, MealDetailResponse, MealCreateResponse
from app.api.dao import MealDAO, MealFoodItemDAO, FoodItemDAO
from app.core.exceptions import MealNotFound, ForbiddenException, InvalidMealData, FoodItemNotFound

router = APIRouter(
    prefix='/meals',
    tags=['Приёмы пищи 🍽']
    )

# -------------------------------------------
# Вспомогательные функции
# -------------------------------------------

async def _check_meal_ownership(
    session: AsyncSession, 
    meal_id: int, 
    user_id: int
) -> Meal:
    '''Проверяет, принадлежит ли приём пищи пользователю.'''
    meal_dao = MealDAO(session)
    meal = await meal_dao.get_meal_by_id(meal_id)
    if not meal:
        raise MealNotFound(f'Приём пищи с ID {meal_id} не найден')
    if meal.user_id != user_id:
        raise ForbiddenException()
    return meal

# -------------------------------------------
# Эндпоинты
# -------------------------------------------

@router.post('/add', response_model=MealCreateResponse, summary='Добавить приём пищи')
async def create_meal(
    data: MealCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit),
):
    if not await FoodItemDAO(session).find_one_by_fields(id=data.food_item_id):
        raise FoodItemNotFound(data.food_item_id)

    try:
        meal_id = await MealDAO(session).create_meal(
            user_id=current_user.id,
            food_item_id=data.food_item_id,
            mealtime=data.mealtime,
            meal_date=data.meal_date,
            quantity=data.quantity
        )
        return {
            'message': f'Прием пищи под ID {meal_id} добавлен успешно!',
            'meal_id': meal_id
        }
    except SQLAlchemyError as e:
        raise HTTPException(500, 'Ошибка сохранения')



@router.delete('/delete/{meal_id}', summary='Удалить приём пищи')
async def delete_meal(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit),
):
    '''
    Удаляет приём пищи и все связанные записи.
    '''
    await _check_meal_ownership(session, meal_id, current_user.id)
    meal_dao = MealDAO(session)
    await meal_dao.delete_meal(meal_id)
    return {'message': 'Приём пищи успешно удалён'}



@router.get('/get_date/{date}', summary='Получить все приёмы пищи в определенную дату', response_model=List[MealDetailResponse])
async def get_meals_by_date(
    date: date = Path(..., description='Дата в формате YYYY-MM-DD'),  # Тип date!
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_without_commit),
):
    try:
        meals = await MealDAO(session).get_meals_by_date(
            user_id=current_user.id,
            target_date=date  # Передаем date напрямую
        )
        if not meals:
            raise MealNotFound('Приемы пищи не найдены')
        return meals
    except SQLAlchemyError as e:
        logger.error(f'Database error: {e}')
        raise HTTPException(500, 'Ошибка при получении данных')



@router.post('/{meal_id}/add_food', summary='Добавить продукт к приему пищи')
async def add_food_to_meal(
    meal_id: int,
    food_item_id: int = Body(..., gt=0),
    quantity: float = Body(..., gt=0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit),
):
    await _check_meal_ownership(session, meal_id, current_user.id)
    
    food_item = await FoodItemDAO(session).get_food_item_by_id(food_item_id)
    if not food_item:
        raise FoodItemNotFound(food_item_id)
    
    try:
        await MealFoodItemDAO(session).add_food_to_meal(
            meal_id=meal_id,
            food_item_id=food_item_id,
            quantity=quantity
        )
        return {'message': 'Продукт добавлен'}
    except InvalidMealData as e:
        raise HTTPException(400, detail=str(e))


@router.delete('/{meal_id}/remove_food/{food_item_id}', summary='Удалить продукт из приёма пищи')
async def remove_food_from_meal(
    meal_id: int,
    food_item_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit),
):
    '''
    Удаляет продукт из приёма пищи.
    '''
    await _check_meal_ownership(session, meal_id, current_user.id)
    meal_food_item_dao = MealFoodItemDAO(session)
    await meal_food_item_dao.remove_food_from_meal(
        meal_id=meal_id,
        food_item_id=food_item_id
    )
    return {'message': 'Продукт успешно удалён'}


@router.put('/update/{meal_id}', summary='Обновить приём пищи')
async def update_meal(
    meal_id: int,
    mealtime: Mealtime | None = None,
    meal_date: datetime | None = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit),
):
    '''
    Обновляет данные приёма пищи (время или тип).
    '''
    await _check_meal_ownership(session, meal_id, current_user.id)
    meal_dao = MealDAO(session)
    await meal_dao.update_meal(
        meal_id=meal_id,
        mealtime=mealtime,
        meal_date=meal_date
    )
    return {'message': 'Данные обновлены'}