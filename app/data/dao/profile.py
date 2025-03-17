from fastapi import HTTPException
from app.models import Profile, User
from app.data.dao import BaseDAO
from app.schemas.profiles import ProfileInfoResponse, UpdateProfileRequest

class ProfileDAO(BaseDAO[Profile]):
    model = Profile


    async def get_role_and_fullname(self, user: User) -> dict:
        '''Получить полное имя (name + lastname) текущего пользователя в формате JSON.'''
        if not user.profile:
            raise HTTPException(status_code=404, detail='Profile not found')
    
        full_name = f'{user.profile.name} {user.profile.last_name}'
        return {'full_name': full_name}  # Возвращаем словарь с ключом full_name
    

    async def get_profile_info(self, user: User) -> ProfileInfoResponse:
        '''Получить информацию о профиле пользователя.'''
        if not user.profile:
            raise HTTPException(status_code=404, detail='Profile not found')
        
        return ProfileInfoResponse(
            name=user.profile.name,
            last_name=user.profile.last_name,
            gender=user.profile.gender.value,
            weight=user.profile.weight,
            height=user.profile.height,
            birthday_date=user.profile.birthday_date
        )

    async def update_profile(
        self,
        user: User,
        profile_data: UpdateProfileRequest
    ) -> dict:
        '''Обновить информацию профиля пользователя.'''
        profile = await self.find_one_by_fields(user_id=user.id)
        if not profile:
            raise HTTPException(status_code=404, detail='Профиль не найден!')
        
        for key, value in profile_data.model_dump(exclude_unset=True).items():
            setattr(profile, key, value)
        
        await self._session.commit()
        return {'message': 'Профиль успешно обновлен!'}