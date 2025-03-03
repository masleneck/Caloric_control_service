from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.schemas.users import UserCreate, UserResponse
from app.crud.users import create_user, get_user_by_username
from app.core.security import verify_password, create_access_token
from app.core.db import get_async_session
from app.core.config import settings

router = APIRouter(
    prefix='/auth', 
    tags=['Аутентификация 🛡️']
    )


@router.post(
        '/register',
        tags=['Аутентификация 🛡️'],
        summary='🟢 Регистрация нового пользователя',
        response_model=UserResponse
        )
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_async_session))-> UserResponse:
    '''Регистрация пользователя'''
    new_user = await create_user(session, user_data)
    return new_user


@router.post(
        '/token',
        tags=['Аутентификация 🛡️'],
        summary='🔑 Получить токен доступа (login)',
        )
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)) -> dict[str, str]: # Возвращаем словарь с токеном и типом
    '''Авторизация пользователя по username и password'''
    user = await get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Неверный логин или пароль')
    access_token = create_access_token(
        data={'sub': user.username}, 
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
    return {'access_token': access_token, 'token_type': 'bearer'}



'''
Как будет работать вход в систему (логин)?
Если у нас есть HTML-форма для входа (например, на login.html), то процесс будет следующим:

Пользователь вводит логин и пароль в форму на сайте.
Форма отправляет данные (username, password) на бэкенд через POST-запрос.
Бэкенд обрабатывает запрос на /auth/token, проверяет логин и пароль.
Если все ок, сервер возвращает access_token, который используется для дальнейшей работы (например, для доступа в личный кабинет).
Фронтенд сохраняет токен (например, в localStorage или cookies) и использует его для авторизованных запросов.
'''