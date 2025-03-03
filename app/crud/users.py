from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate, UserUpdateAdmin, UserResponse, UserRole


async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
    '''Получает пользователя по ID.'''
    result = await session.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    '''Получает пользователя по username.'''
    result = await session.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    '''Получает пользователя по email.'''
    result = await session.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def update_user(session: AsyncSession, user: User, user_data: UserUpdate) -> User:
    '''Обновляет данные текущего пользователя'''
    update_data = user_data.model_dump(exclude_unset=True)
    if not update_data:
        return user  # Если нечего обновлять, просто возвращаем пользователя
    validated_user = UserUpdate.model_validate(update_data)  # Валидация перед изменением
    for key, value in validated_user.model_dump().items():
        setattr(user, key, value)
    await session.commit()  # Фиксируем изменения
    await session.refresh(user)  # Обновляем объект из БД
    return user


async def get_all_users(session: AsyncSession) -> list[UserResponse]:
    '''Получает список всех пользователей (admin)'''
    result = await session.execute(select(User)) # SELECT * FROM users
    users = result.scalars().all() # извлекает только объекты модели User, игнорируя метаданные запроса
    return [UserResponse.model_validate(user) for user in users] # Обходим всех пользователей (for user in users) 
    # Преобразуем каждый объект User в валидный UserResponse. model_validate(user) — конвертирует SQLAlchemy-объект в Pydantic-схему.


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    from core.security import get_password_hash # ⚠️ ПОТОМ ФИКС ⚠️
    '''Создает нового пользователя (admin)'''
    if await get_user_by_username(session, user_data.username):
        raise HTTPException(status_code=400, detail='Имя пользователя уже занято')
    if await get_user_by_email(session, user_data.email):
        raise HTTPException(status_code=400, detail='Email уже используется')
    hashed_password = get_password_hash(user_data.password)  # Хешируем пароль перед сохранением
    user_data_dict = user_data.model_dump(exclude={'password'}, exclude_unset=True)
    new_user = User(**user_data_dict, hashed_password=hashed_password) # Создаем объект пользователя
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user) 
    return new_user


async def delete_user(session: AsyncSession, username: str)-> None:
    '''Удаляет пользователя по username (admin)'''
    user = await get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    await session.delete(user) 
    await session.commit()



async def update_user_admin(session: AsyncSession, username: str, user_data: UserUpdateAdmin) -> Optional[User]:
    '''Обновляет данные пользователя по username (admin)'''
    user = await get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    update_data = user_data.model_dump(exclude_unset=True)
    if not update_data:
        return user  # Если нечего обновлять, просто возвращаем пользователя
    validated_user = UserUpdateAdmin.model_validate(update_data)  # Валидация перед изменением
    for key, value in validated_user.model_dump().items():
        setattr(user, key, value)
    await session.commit()  # Фиксируем изменения
    await session.refresh(user)  # Обновляем объект из БД
    return user


async def change_role(session: AsyncSession, username: str, user_data: UserRole) -> Optional[User]:
    '''Обновляет роль пользователя по username (admin)'''
    user = await get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    user.role = user_data
    await session.commit() 
    await session.refresh(user)  
    return {'message': f'Роль пользователя {username} изменена на {user_data.value}'}



