from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database_dep import get_async_session
from app.dependencies.auth_dep import get_current_user
from app.repositories.profile import ProfileDAO
from app.models.users import User
from app.repositories.workout import WorkoutDAO
from app.schemas.profile import BmiRequest, FullNameResponse, ProfileInfoResponse, UpdateProfileRequest, StatusResponse
from app.core.calculations import calculate_bmi

router = APIRouter(prefix='/profile', tags=['Профиль 👥'])


@router.get('/r_fullname', response_model=FullNameResponse, summary='Получить полное имя')
async def get_fullname(
    current_user: User = Depends(get_current_user)
) -> FullNameResponse:
    if not current_user.profile:
        raise HTTPException(404, 'Профиль пользователя не найден')
    return FullNameResponse(
        full_name=f'{current_user.profile.name} {current_user.profile.last_name}'
    )


@router.get('/r_status', response_model=StatusResponse, summary='Обновляет и возвращает уровень активности на основе тренировок за последние 7 дней')
async def get_status(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> StatusResponse:
    new_level = await WorkoutDAO(session).update_and_get_activity_level(current_user.id)
    return StatusResponse(status=new_level)


@router.get('/profile_info', response_model=ProfileInfoResponse,summary='Получить информацию о профиле')
async def get_profile_info(
    current_user: User = Depends(get_current_user)
) -> ProfileInfoResponse:
    if not current_user.profile:
        raise HTTPException(404, 'Профиль пользователя не найден')
    return ProfileInfoResponse.model_validate(current_user.profile)

@router.patch(
    "/update_profile",
    summary="Обновить данные профиля",
    response_model=dict[str, str],
)
async def update_profile(
    profile_data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    return await ProfileDAO(session).update_profile(
        user_id=current_user.id,
        profile_data=profile_data
    )


@router.post('/bmi', summary='Подсчет bmi')
async def calculate_bmi_api(data: BmiRequest):
    '''Эндпоинт для расчёта метрик'''
    return calculate_bmi(data.model_dump())

