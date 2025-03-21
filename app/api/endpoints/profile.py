from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.dependencies.auth_dep import get_current_user
from app.data.dao import ProfileDAO
from app.models.users import User
from app.schemas.profiles import FullNameResponse, ProfileInfoResponse, UpdateProfileRequest


router = APIRouter(prefix='/profiles', tags=['Профиль 👥'])


@router.get('/r_fullname', response_model=FullNameResponse, summary='Получить полное имя (name + lastname)')
async def get_fullname(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_without_commit)
) -> FullNameResponse:
    '''Получить полное имя (name + lastname) текущего пользователя в формате JSON.'''
    dao = ProfileDAO(session)
    return await dao.get_role_and_fullname(current_user)


@router.get('/profile_info', response_model=ProfileInfoResponse, summary='Получить информацию о профиле текущего пользователя')
async def get_profile_info(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_without_commit)
) -> ProfileInfoResponse:
    '''Получить информацию о профиле текущего пользователя.'''
    dao = ProfileDAO(session)
    return await dao.get_profile_info(current_user)


@router.put('/update_profile', summary='Обновить информацию профиля текущего пользователя')
async def update_profile(
    profile_data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit)
) -> dict:
    '''Обновить информацию профиля текущего пользователя.'''
    dao = ProfileDAO(session)
    return await dao.update_profile(current_user, profile_data)