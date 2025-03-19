from loguru import logger
from fastapi import HTTPException
from app.data.dao import BaseDAO
from app.models import User, Gender, CurrentGoal, ActivityLevel, Profile
from app.schemas.users import UserRegister, UserAuth, UserInfo, ConfidentialInfoResponse, UpdateConfidentialInfoRequest
from app.core.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.utils.auth_utils import get_password_hash, verify_password

class UserDAO(BaseDAO[User]):
    model = User


    async def get_user_by_email(self, email: str) -> User | None:
        '''Найти пользователя по email.'''
        return await self.find_one_by_fields(email=email)


    async def register_user(self, user_data: UserRegister) -> dict:
        '''Зарегистрировать нового пользователя.'''
        existing_user = await self.find_one_by_fields(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsException

        # Хэшируем пароль
        logger.info('Хэширование пароля для нового пользователя')
        hashed_password = get_password_hash(user_data.password)
        logger.info(f'Хэшированный пароль: {hashed_password}')

        user_data_dict = user_data.model_dump(exclude={'confirm_password', 'fullname'})
        user_data_dict['password'] = hashed_password

        # Создаем пользователя
        logger.info('Создание нового пользователя')
        new_user = self.model(**user_data_dict)
        self._session.add(new_user)
        await self._session.commit()
        await self._session.refresh(new_user)

        # Разделяем fullname на name и last_name
        name = user_data.name.capitalize()
        last_name = user_data.last_name.capitalize()

        # Создаем профиль пользователя
        logger.info('Создание профиля пользователя')
        profile_data = {
        'user_id': new_user.id,
        'name': name,
        'last_name': last_name,
        'gender': Gender.NOT_STATED,
        'weight': 0.0,
        'height': 0,
        'goal': CurrentGoal.NOT_STATED,
        'birthday_date': None,
        'activity_level': ActivityLevel.NOT_STATED,
        }
        new_profile = Profile(**profile_data)
        self._session.add(new_profile)
        await self._session.commit()

        return {'message': 'Вы успешно зарегистрированы!'}


    async def authenticate_user(self, user_data: UserAuth) -> User:
        '''Аутентифицировать пользователя.'''
        logger.info(f'Поиск пользователя по email: {user_data.email}')

        user = await self.find_one_by_fields(email=user_data.email)

        if not user:
            logger.error('Пользователь не найден')
            raise IncorrectEmailOrPasswordException
        else:
            logger.info('Пользователь найден!')
    
        if not verify_password(user_data.password, user.password):
            logger.error('Неверный пароль')
            raise IncorrectEmailOrPasswordException
    
        logger.info(f'Пользователь {user.id} успешно аутентифицирован')
        return user
 
 

    async def get_all_users(self) -> list[UserInfo]:
        '''Получить информацию о всех пользователях.'''
        users = await self.find_all()
        return [UserInfo.model_validate(user) for user in users]


    async def get_confidential_info(self, user: User) -> ConfidentialInfoResponse:
        '''Получить конфиденциальную информацию пользователя.'''
        return ConfidentialInfoResponse(email=user.email, password='******')
    

    async def update_confidential_info(
        self,
        user: User,
        credentials: UpdateConfidentialInfoRequest
    ) -> dict:
        '''Обновить конфиденциальную информацию пользователя.'''
        if user.email != credentials.email or not verify_password(credentials.password, user.password):
            raise HTTPException(status_code=400, detail='Неверный email или password!')
    
        if credentials.new_password != credentials.confirm_new_password:
            raise HTTPException(status_code=400, detail='Пароли не совпадают!')
        # Обновляем email и пароль
        user.email = credentials.new_email
        user.password = get_password_hash(credentials.new_password)
        # Явно добавляем объект в текущую сессию
        merged_user = await self._session.merge(user)
        # Фиксируем изменения в базе данных
        await self._session.commit()

        return {'message': 'Конфиденциальные данные изменены успешно!'}