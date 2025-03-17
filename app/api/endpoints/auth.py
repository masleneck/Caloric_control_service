from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.utils.token_utils import set_tokens
from app.dependencies.auth_dep import get_current_user, get_current_admin_user, check_refresh_token
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.schemas.users import UserRegister, UserAuth, UserInfo, ConfidentialInfoResponse, UpdateConfidentialInfoRequest
from app.data.dao import UserDAO

router = APIRouter(
    prefix='/auth',
    tags=['Аутентификация 🛡️']
)

@router.post('/register/', summary='Регистрация пользователя')
async def register_user(
    user_data: UserRegister,
    session: AsyncSession = Depends(get_session_with_commit)
) -> dict:
    """Зарегистрировать нового пользователя."""
    dao = UserDAO(session)
    return await dao.register_user(user_data)

@router.post('/login/', summary='Аутентификация пользователя')
async def auth_user(
    response: Response,
    user_data: UserAuth,
    session: AsyncSession = Depends(get_session_without_commit)
) -> dict:
    """Аутентифицировать пользователя."""
    dao = UserDAO(session)
    user = await dao.authenticate_user(user_data)
    set_tokens(response, user.id)
    return {'ok': True, 'message': 'Авторизация успешна!'}

@router.post('/logout', summary='Выйти из системы')
async def logout(response: Response) -> dict:
    """Выйти из системы."""
    response.delete_cookie('user_access_token')
    response.delete_cookie('user_refresh_token')
    return {'message': 'Пользователь успешно вышел из системы'}

@router.get('/all_users/', summary='🚨 Получить информацию о всех пользователях')
async def get_all_users(
    session: AsyncSession = Depends(get_session_with_commit),
    current_user: User = Depends(get_current_admin_user)
) -> list[UserInfo]:
    """Получить информацию о всех пользователях."""
    dao = UserDAO(session)
    return await dao.get_all_users()

@router.post('/refresh', summary='Обновить токены')
async def process_refresh_token(
    response: Response,
    user: User = Depends(check_refresh_token)
) -> dict:
    """Обновить токены."""
    set_tokens(response, user.id)
    return {'message': 'Токены успешно обновлены'}




@router.get('/confidential_info', response_model=ConfidentialInfoResponse)
async def get_confidential_info(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_without_commit)
):
    '''Получить конфиденциальную информацию текущего пользователя.'''
    dao = UserDAO(session)
    return await dao.get_confidential_info(current_user)


# @router.put('/update_confidential_info')
# async def update_confidential_info(
#     credentials: UpdateConfidentialInfoRequest,
#     current_user: User = Depends(get_current_user),
#     session: AsyncSession = Depends(get_session_with_commit)
# ):
#     '''Обновить конфиденциальную информацию текущего пользователя.'''
#     dao = UserDAO(session)
#     return await dao.update_confidential_info(current_user, credentials)