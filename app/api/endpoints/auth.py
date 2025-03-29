from typing import Annotated
from loguru import logger
from fastapi import APIRouter, Response, Depends, Cookie, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database_dep import get_async_session
from app.models import User
from app.utils.token_utils import set_tokens
from app.dependencies.auth_dep import get_current_user, get_current_admin_user, check_refresh_token
from app.schemas.users import UserRegister, UserAuth, UserInfo, ConfidentialInfoResponse, UpdateConfidentialInfoRequest
from app.repositories.user import UserDAO
from app.api.endpoints.profile import router as profile_router

router = APIRouter(
    prefix='/auth',
    tags=['Аутентификация 🛡️']
)


@router.post('/register', summary='Регистрация пользователя')
async def register_user(
    user_data: UserRegister,
    response: Response,
    session_id: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    if not session_id:
        raise HTTPException(status_code=400, detail='Требуется session_id')
    
    try:
        result = await UserDAO(session).register_user(user_data, session_id)
        response.delete_cookie(key='session_id')
        return result
    finally:
        await session.close()  # Гарантированное закрытие сессии


@router.post('/login', summary='Аутентификация пользователя')
async def auth_user(
    response: Response,
    user_data: UserAuth,
    session: AsyncSession = Depends(get_async_session),
) -> dict:  
    try:
        dao = UserDAO(session)
        user = await dao.authenticate_user(user_data)
        set_tokens(response, user.id)
        
        return {
            'ok': True,
            'message': 'Авторизация успешна!',
            'user_id': user.id
        }
    finally:
        await session.close()


@router.post('/logout', summary='Выйти из системы')
async def logout(response: Response) -> dict:
    '''Выйти из системы.'''
    response.delete_cookie('user_access_token')
    response.delete_cookie('user_refresh_token')
    return {'message': 'Пользователь успешно вышел из системы'}


@router.post('/refresh', summary='Обновить токены')
async def process_refresh_token(
    response: Response,
    user: User = Depends(check_refresh_token)
) -> dict:
    '''Обновить токены.'''
    set_tokens(response, user.id)
    return {'message': 'Токены успешно обновлены'}


@profile_router.get(
    '/confidential_info',
    response_model=ConfidentialInfoResponse,
    summary='Получить конфиденциальные данные',
)
async def get_confidential_info(
    current_user: User = Depends(get_current_user)
) -> ConfidentialInfoResponse:
    """
    Получение конфиденциальной информации пользователя
    """
    return ConfidentialInfoResponse(
        email=current_user.email,
        password='******'  
    )


@profile_router.put('/update_confidential_info')
async def update_confidential_info(
    update_data: UpdateConfidentialInfoRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        return await UserDAO(session).update_credentials(current_user, update_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update error: {e}")
        raise HTTPException(500, "Ошибка сервера")
    finally:
        await session.close()


@router.get(
    '/users',
    response_model=list[UserInfo],
    summary='Список пользователей (is_superuser)',
)
async def admin_get_users(
    skip: Annotated[int, Query(ge=0, description="Смещение")] = 0,
    limit: Annotated[int, Query(le=200, description="Лимит")] = 100,
    sort_by: Annotated[str, Query(description="Сортировка (id/email/name)")] = 'id',
    current_admin: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_async_session)
) -> list[UserInfo]:
    logger.info(f"Admin #{current_admin.id} requested users list")
    
    return await UserDAO(session).get_all_users(
        skip=skip,
        limit=limit,
        sort_by=sort_by
    )