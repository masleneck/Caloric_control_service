from loguru import logger
from fastapi import APIRouter, Response, Depends, Cookie, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.utils.token_utils import set_tokens
from app.dependencies.auth_dep import get_current_user, get_current_admin_user, check_refresh_token
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.schemas.users import UserRegister, UserAuth, UserInfo, ConfidentialInfoResponse, UpdateConfidentialInfoRequest
from app.data.dao import UserDAO
from app.api.endpoints.profile import router as profile_router

router = APIRouter(
    prefix='/auth',
    tags=['Аутентификация 🛡️']
)


@router.post('/register/', summary='Регистрация пользователя')
async def register_user(
    user_data: UserRegister,
    response: Response,
    session_id: str | None = Cookie(default=None),  # Извлекаем session_id из cookies
    session: AsyncSession = Depends(get_session_with_commit)
) -> dict:
    '''Зарегистрировать нового пользователя.'''
    if not session_id:
        raise HTTPException(status_code=400, detail='Требуется идентификатор сеанса')
    # Передаем session_id в DAO
    result = await UserDAO(session).register_user(user_data, session_id)
    # Удаляем куку session_id
    response.delete_cookie(key='session_id')

    return result


@router.post('/login/', summary='Аутентификация пользователя')
async def auth_user(
    response: Response,
    user_data: UserAuth,
    session: AsyncSession = Depends(get_session_without_commit)
) -> dict:
    '''Аутентифицировать пользователя.'''
    dao = UserDAO(session)
    user = await dao.authenticate_user(user_data)
    set_tokens(response, user.id)
    return {'ok': True, 
            'message': 'Авторизация успешна!',
            'user_id': user.id
    }


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


@router.get('/all_users/', summary='🚨 Получить информацию о всех пользователях')
async def get_all_users(
    skip: int = Query(0, description='Количество записей для пропуска'),
    limit: int = Query(100, description='Лимит записей на странице'),
    sort_by: str = Query('id', description='Поле для сортировки (id, email, name)'),
    session: AsyncSession = Depends(get_session_without_commit),
    current_user: User = Depends(get_current_admin_user)
) -> list[UserInfo]:
    '''
    Получить информацию о всех пользователях.
    Доступно только для администраторов.
    '''
    # Логируем запрос
    logger.info(f'Администратор {current_user.id} запросил список пользователей')

    dao = UserDAO(session)
    return await dao.get_all_users(skip=skip, limit=limit, sort_by=sort_by)


@profile_router.get('/confidential_info', response_model=ConfidentialInfoResponse, summary='Получить конфиденциальную информацию текущего пользователя')
async def get_confidential_info(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_without_commit)
) -> ConfidentialInfoResponse:
    '''Получить конфиденциальную информацию текущего пользователя.'''
    dao = UserDAO(session)
    return await dao.get_confidential_info(current_user)


@profile_router.put('/update_confidential_info',summary='Обновить конфиденциальную информацию текущего пользователя')
async def update_confidential_info(
    credentials: UpdateConfidentialInfoRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit)
) -> dict:
    '''Обновить конфиденциальную информацию текущего пользователя.'''
    dao = UserDAO(session)
    return await dao.update_confidential_info(current_user, credentials)