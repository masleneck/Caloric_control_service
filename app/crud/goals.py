from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.models.goals import Goal
from app.schemas.goals import GoalUpdate, GoalResponse



async def get_goal_by_id(session: AsyncSession, goal_id: int) -> Optional[Goal]:
    '''Возвращает цель по ID'''
    goal = await session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail='Цель не установлена')
    return goal


async def get_all_goals(session: AsyncSession) -> List[GoalResponse]:
    '''Получает список всех целей'''
    result = await session.execute(select(Goal))
    goals = result.scalars().all()
    return [GoalResponse.model_validate(goal) for goal in goals]


# async def update_goal(session: AsyncSession, goal_id: int, goal_data: GoalUpdate) -> Optional[Goal]:
#     '''Обновляет информацию о цели'''
#     result = await session.execute(select(Goal).filter(Goal.id == goal_id))
#     goal = result.scalars().first()
#     if not goal:
#         raise HTTPException(status_code=404, detail='Продукт не найден')
#     validated_food = GoalUpdate.model_validate(goal_data) 
#     for key, value in validated_food.model_dump().items():
#         setattr(goal, key, value)
#     await session.commit()
#     await session.refresh(goal)
#     return goal

