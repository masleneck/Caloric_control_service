from datetime import datetime, timezone
from fastapi import Request, Depends, Response
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserDAO
from app.models.users import User
from app.core.config import settings
from app.dependencies.database_dep import get_async_session
from app.core.exceptions import TokenNotFoundException, InvalidJwtTokenException, TokenExpiredException, ForbiddenException, UserNotFoundException
from app.utils.token_utils import set_tokens


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
        session: AsyncSession = Depends(get_async_session)
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
        request: Request,
        response: Response,
        token: str = Depends(get_access_token),
        session: AsyncSession = Depends(get_async_session)
) -> User:
    '''Проверяем access_token и возвращаем пользователя. Если access_token истек, используем refresh_token для обновления токенов.
    не безопасно ибо шлем рефрештокены в каждом запросе!'''
    try:
        # Декодируем токен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get('sub')
        if not user_id:
            raise UserNotFoundException

        user = await UserDAO(session).find_one_or_none_by_id(data_id=int(user_id))
        if not user:
            raise UserNotFoundException

        return user
    except ExpiredSignatureError:
        # Access token expired, try to refresh using refresh token
        refresh_token = request.cookies.get('user_refresh_token')
        if refresh_token:
            try:
                refresh_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                refresh_user_id = refresh_payload.get('sub')
                if not refresh_user_id:
                    raise InvalidJwtTokenException

                refresh_user = await UserDAO(session).find_one_or_none_by_id(data_id=int(refresh_user_id))
                if not refresh_user:
                    raise UserNotFoundException

                # Set new tokens in response cookies
                set_tokens(response, user_id=int(refresh_user_id))
                return refresh_user
            except ExpiredSignatureError:
                raise TokenExpiredException  # Refresh token expired
            except JWTError:
                raise InvalidJwtTokenException  # Invalid refresh token
        else:
            raise TokenExpiredException  # No refresh token available
    except JWTError:
        raise InvalidJwtTokenException  # Invalid access token
    
    
async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    '''Проверяем права пользователя как администратора.'''
    if current_user.is_superuser:   # Проверяем, что роль пользователя — ADMIN
        return current_user
    raise ForbiddenException