from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from app.core.security import get_current_user, is_admin
from app.core.db import get_async_session
from app.crud.goals import get_goal_by_id, get_all_goals
from app.models.users import User
from app.schemas.goals import GoalResponse


router = APIRouter(
    prefix='/goal',
    tags=['Цели 🎯']
    )


@router.get(
        '/get/{food_id}',
        tags=['Цели 🎯'],
        summary='Получить цель по ID',
        response_model=GoalResponse
        )
async def get_goal(
    goal_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Позволяет пользователю получить свою цель по ID '''
    return await get_goal_by_id(session, goal_id)


@router.get(
        '/list',
        tags=['Цели 🎯'],
        summary='Получить цель по ID',
        response_model=List[GoalResponse]
        )
async def get_goal_list(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Позволяет пользователю получить список всех целей'''
    return await get_all_goals(session)


# @router.put(
#         '/update/{food_id}',
#         tags=['Цели 🎯'],
#         summary='Обновить информацию цели',
#         response_model=GoalResponse
#         )
# async def update_food_info(
#     food_id: int,
#     food_data: FoodCreate,
#     session: AsyncSession = Depends(get_async_session),
#     admin_user: User = Depends(is_admin)  
#     ):
#     '''Позволяет администратору обновить информацию о продукте'''
#     return await update_food(session, food_id, food_data)