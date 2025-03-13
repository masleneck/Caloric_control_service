from datetime import datetime, timezone
from fastapi import Request, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dao import UserDAO
from app.models.users import User, Role
from app.core.config import settings
from app.dependencies.dao_dep import get_session_without_commit
from app.core.exceptions import TokenNotFoundException, InvalidJwtTokenException, TokenExpiredException, UserIdNotFoundException, ForbiddenException, UserNotFoundException


def get_access_token(request: Request) -> str:
    '''Извлекаем access_token из кук.'''
    token = request.cookies.get('user_access_token')
    if not token:
        raise TokenNotFoundException
    return token


def get_refresh_token(request: Request) -> str:
    '''Извлекаем refresh_token из кук.'''
    token = request.cookies.get('user_refresh_token')
    if not token:
        raise TokenNotFoundException
    return token


async def check_refresh_token(
        token: str = Depends(get_refresh_token),
        session: AsyncSession = Depends(get_session_without_commit)
) -> User:
    ''' Проверяем refresh_token и возвращаем пользователя.'''
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get('sub')
        if not user_id:
            raise InvalidJwtTokenException

        user = await UserDAO(session).find_one_or_none_by_id(data_id=int(user_id))
        if not user:
            raise InvalidJwtTokenException

        return user
    except JWTError:
        raise InvalidJwtTokenException


async def get_current_user(
        token: str = Depends(get_access_token),
        session: AsyncSession = Depends(get_session_without_commit)
) -> User:
    '''Проверяем access_token и возвращаем пользователя.'''
    try:
        # Декодируем токен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        # Общая ошибка для токенов
        raise InvalidJwtTokenException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIdNotFoundException

    user = await UserDAO(session).find_one_or_none_by_id(data_id=int(user_id))
    if not user:
        raise UserNotFoundException
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    '''Проверяем права пользователя как администратора.'''
    if current_user.role in [Role.ADMIN]:  # Проверяем, что роль пользователя — ADMIN
        return current_user
    raise ForbiddenException