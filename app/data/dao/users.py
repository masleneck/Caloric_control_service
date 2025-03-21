from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import load_only
from fastapi import HTTPException
from app.data.dao import BaseDAO
from app.models import User, Gender, CurrentGoal, ActivityLevel, Profile, TestResult
from app.schemas.users import UserRegister, UserAuth, UserInfo, ConfidentialInfoResponse, UpdateConfidentialInfoRequest
from app.core.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.utils.auth_utils import get_password_hash, verify_password

class UserDAO(BaseDAO[User]):
    model = User

    async def register_user(self, user_data: UserRegister, session_id: str) -> dict:
        '''Зарегистрировать нового пользователя.'''
        # Проверяем, существует ли TestResult с таким session_id
        test_result = await self._session.execute(
            select(TestResult).where(TestResult.session_id == session_id)
        )
        test_result = test_result.scalars().first()
        
        if not test_result:
            raise HTTPException(status_code=400, detail='Неверный идентификатор сеанса')

        # Проверяем, существует ли пользователь с таким email
        existing_user = await self.find_one_by_fields(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsException
        
        # Хэшируем пароль
        # logger.info('Хэширование пароля для нового пользователя')
        hashed_password = get_password_hash(user_data.password)
        # logger.info(f'Хэшированный пароль: {hashed_password}')

        # Создаем словарь для данных пользователя, исключая confirm_password и fullname
        user_data_dict = user_data.model_dump(exclude={'confirm_password', 'fullname'})
        user_data_dict['password'] = hashed_password

        # Создаем пользователя
        # logger.info('Создание нового пользователя')
        new_user = self.model(**user_data_dict)
        self._session.add(new_user)
        await self._session.flush()  # Получаем ID нового пользователя

        # Разделяем fullname на name и last_name
        name = user_data.name.capitalize()
        last_name = user_data.last_name.capitalize() if user_data.last_name else None

        # Создаем профиль пользователя
        # logger.info('Создание профиля пользователя')
        profile_data = {
        'user_id': new_user.id,
        'name': name,
        'last_name': last_name,
        'gender': test_result.gender,  # Используем данные из TestResult
        'weight': test_result.weight,
        'height': test_result.height,
        'goal': test_result.goal,
        'birthday_date': test_result.birthday_date,
        'activity_level': ActivityLevel.NOT_STATED,  # По умолчанию
        }
        new_profile = Profile(**profile_data)
        self._session.add(new_profile)

        # Связываем TestResult с пользователем
        test_result.user_id = new_user.id
        
        # Удаляем запись из test_results
        await self._session.delete(test_result)
        
        return {'message': 'Вы успешно зарегистрированы!'}


    async def authenticate_user(self, user_data: UserAuth) -> User:
        '''Аутентифицировать пользователя.'''
        # logger.info(f'Поиск пользователя по email: {user_data.email}')
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
        
        merged_user = await self._session.merge(user)
        await self._session.commit()

        return {'message': 'Конфиденциальные данные изменены успешно!'}
    

    async def get_all_users(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = 'id'
    ) -> list[UserInfo]:
        '''
        Получить информацию о всех пользователях.

        Args:
            skip (int): Количество записей для пропуска (пагинация).
            limit (int): Лимит записей на странице (пагинация).
            sort_by (str): Поле для сортировки (id, email, name).

        Returns:
            list[UserInfo]: Список пользователей.
        '''
        # Определяем поле для сортировки
        sort_field = getattr(User, sort_by, User.id)

        # Формируем запрос с пагинацией и сортировкой
        query = (
            select(User)
            .order_by(sort_field)
            .offset(skip)
            .limit(limit)
        )
        # Выполняем запрос
        result = await self._session.execute(query)
        users = result.scalars().all()

        # Преобразуем в список UserInfo
        return [UserInfo.model_validate(user) for user in users]