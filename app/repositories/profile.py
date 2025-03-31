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
        user_id: int,
        profile_data: UpdateProfileRequest
    ) -> dict[str, str]:
        result = await self._session.execute(
            select(User)
            .options(selectinload(User.profile))
            .where(User.id == user_id)
        )
        user = result.scalars().first()

        if not user or not user.profile:
            raise HTTPException(status_code=404, detail='Профиль не найден!')

        update_data = profile_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            # Игнорируем пустые строки
            if isinstance(value, str) and not value.strip():
                continue
    
            # Проверяем, отличается ли новое значение от текущего
            current_value = getattr(user.profile, field)
            if current_value != value:
                setattr(user.profile, field, value)
                
        await self._session.commit()
        return {'message': 'Профиль успешно обновлен!'}