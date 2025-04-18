from datetime import date
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.repositories.workout import WorkoutDAO
from app.dependencies.database_dep import get_async_session
from app.dependencies.auth_dep import get_current_admin_user, get_current_user
from app.schemas.workouts import DailyWorkoutsResponse, DailyWorkoutsSummaryResponse, WorkoutResponse, WorkoutUpsertRequest, WorkoutSearchItemResponse

router = APIRouter(
   prefix='/workouts',
   tags=['Тренировки 💪🏼']
)


@router.post("/upsert_workout", response_model=WorkoutResponse, summary="Обновить/Создать тренировку")
async def upsert_workout(
    workout_data: WorkoutUpsertRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await WorkoutDAO(session).upsert_workouts(user.id, workout_data)


@router.get("/search_item", response_model=List[WorkoutSearchItemResponse], summary="Поиск схожих тренировок")
async def search_foods(
    query: str = Query(..., min_length=2, max_length=50),
    limit: int = Query(10, ge=1, le=50),
    session: AsyncSession = Depends(get_async_session)
):
    '''Поиск тренировок'''
    return await WorkoutDAO(session).search_workouts(query=query, limit=limit)

@router.get("/daily_summary",summary="Получает суммарную информацию о тренировках за день")
async def get_daily_workouts_summary(
    target_date: date ,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> DailyWorkoutsSummaryResponse:
    return await WorkoutDAO(session).get_daily_workouts_summary(user.id, target_date)


@router.get("/daily_workouts",response_model=DailyWorkoutsResponse,summary="Получает список всех тренировок за день")
async def get_daily_workouts(
    target_date: date ,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> DailyWorkoutsResponse:
    return await WorkoutDAO(session).get_daily_workouts(user.id, target_date)



@router.delete("/delete_workout", summary="Удалить тренировку по названию и дате")
async def delete_workout(
    workout_name: str,
    workout_date: date,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    await WorkoutDAO(session).delete_workout_by_name_and_date(
        workout_name=workout_name,
        workout_date=workout_date,
        user_id=user.id
    )
    return {"message": f"Тренировка '{workout_name}' за {workout_date} успешно удалена!"}