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