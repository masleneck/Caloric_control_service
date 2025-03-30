from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models import Profile, User
from app.repositories.base import BaseDAO
from app.schemas.profile import ProfileInfoResponse, UpdateProfileRequest

class ProfileDAO(BaseDAO[Profile]):
    model = Profile


    async def get_profile_info(self, user: User) -> ProfileInfoResponse:
        '''Получить информацию о профиле пользователя.'''
        # Загружаем пользователя с профилем
        query = (
            select(User)
            .options(selectinload(User.profile))  # Загружаем связанный профиль
            .where(User.id == user.id)
        )
        result = await self._session.execute(query)
        user_with_profile = result.scalars().first()

        if not user_with_profile or not user_with_profile.profile:
            raise HTTPException(status_code=404, detail='Профиль пользователя не найден')

        return ProfileInfoResponse(
            name=user_with_profile.profile.name,
            last_name=user_with_profile.profile.last_name,
            gender=user_with_profile.profile.gender.value,
            weight=user_with_profile.profile.weight,
            height=user_with_profile.profile.height,
            goal=user_with_profile.profile.goal,
            birthday_date=user_with_profile.profile.birthday_date
        )


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