from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from app.models.users import User, UserRole
from app.schemas.users import UserResponse, UserUpdate, UserCreate, UserUpdateAdmin
from app.crud.users import update_user, get_all_users, delete_user, create_user, update_user_admin, change_role
from app.core.security import get_current_user, is_admin
from app.core.db import get_async_session

router = APIRouter(
    prefix='/users', 
    tags=['Пользователи 🧍']
    )


@router.get(
        '/show_me',
        tags=['Пользователи 🧍'],
        summary='Показать информацию о текущем пользователе',
        response_model=UserResponse
        )
async def read_users_me(
    current_user: UserResponse = Depends(get_current_user),
    ):
    '''Возвращает информацию о текущем пользователе (если прошел авторизацию).'''
    return current_user


@router.put(
        '/update_me',
        tags=['Пользователи 🧍'],
        summary='Изменить информацию о текущем пользователе',
        response_model=UserResponse
        )
async def update_current_user(
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Позволяет пользователю обновить свои данные'''
    return await update_user(session, current_user, user_data)  # Передаём объект User  


@router.get(
        '/get',
        tags=['Пользователи 🧍'],
        summary='🟢 Получение всех пользователей',
        response_model=List[UserResponse])
async def get_all_users_admin(
    session: AsyncSession = Depends(get_async_session), 
    admin_user: User = Depends(is_admin) # Админская проверка
    ):
    '''Возвращает список всех пользователей (admin).'''
    return await get_all_users(session)


@router.post(
        '/add', 
        tags=['Пользователи 🧍'],
        summary='🟢 Добавление нового пользователя',
        response_model=UserResponse,
        )
async def create_user_admin(
    user_data: UserCreate, 
    session: AsyncSession = Depends(get_async_session), 
    admin_user: User = Depends(is_admin) 
    ):
    '''Создает нового пользователя вручную (admin).'''
    return await create_user(session, user_data)


@router.put(
        '/update/{username}',
        tags=['Пользователи 🧍'],
        summary='🟢 Обновление данных пользователя',
        response_model=UserResponse
        )
async def update_user_for_admin(
    username: str, 
    user_data: UserUpdateAdmin, 
    session: AsyncSession = Depends(get_async_session), 
    admin_user: User = Depends(is_admin) 
    ):
    '''Обновляет данные пользователя (admin).'''
    return await update_user_admin(session, username, user_data)


@router.put(
        '/role/{username}',
        tags=['Пользователи 🧍'],
        summary='🟢 Изменяет роль пользователя ',
        )
async def update_user_role(
    username: str,
    user_data: UserRole,
    session: AsyncSession = Depends(get_async_session),
    admin_user = Depends(is_admin)
    ):
    '''Изменяет роль пользователя по username (admin).'''
    return await change_role(session, username, user_data) 


@router.delete(
        '/delete/{username}',
        tags=['Пользователи 🧍'],
        summary='🟢 Удаление пользователя'
        )
async def delete_user_admin(
    username: str, 
    session: AsyncSession = Depends(get_async_session), 
    admin_user: User = Depends(is_admin)
    ):
    '''Удаляет пользователя (admin).'''
    await delete_user(session, username)
    return {'message': f'Пользователь {username} удален'}

