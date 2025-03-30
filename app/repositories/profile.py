from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from app.models import Profile
from app.models.users import User
from app.repositories.base import BaseDAO
from app.schemas.profile import UpdateProfileRequest
from loguru import logger

class ProfileDAO(BaseDAO[Profile]):
    model = Profile

class ProfileDAO(BaseDAO[Profile]):
    model = Profile

    async def update_profile(
        self,
        user: User,
        profile_data: UpdateProfileRequest
    ) -> dict:
        '''Обновить информацию профиля пользователя.'''
        # Загружаем пользователя с профилем
        query = (
            select(User)
            .options(selectinload(User.profile))  # Загружаем связанный профиль
            .where(User.id == user.id)
        )
        result = await self._session.execute(query)
        user_with_profile = result.scalars().first()

        if not user_with_profile or not user_with_profile.profile:
            raise HTTPException(status_code=404, detail='Профиль не найден!')

        # Обновляем только переданные поля
        for key, value in profile_data.model_dump(exclude_unset=True).items():
            setattr(user_with_profile.profile, key, value)

        return {'message': 'Профиль успешно обновлен!'}

