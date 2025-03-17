from fastapi import HTTPException
from app.data.dao import BaseDAO
from app.models import User
from app.schemas.users import UserRegister, UserAuth, UserInfo, ConfidentialInfoResponse, UpdateConfidentialInfoRequest
from app.core.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.utils.auth_utils import get_password_hash, verify_password

class UserDAO(BaseDAO[User]):
    model = User

    async def get_user_by_email(self, email: str) -> User | None:
        """Найти пользователя по email."""
        return await self.find_one_by_fields(email=email)

    async def register_user(self, user_data: UserRegister) -> dict:
        """Зарегистрировать нового пользователя."""
        existing_user = await self.find_one_by_fields(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsException

        # Хэшируем пароль
        hashed_password = get_password_hash(user_data.password)
        user_data_dict = user_data.model_dump(exclude={'confirm_password'})
        user_data_dict['password'] = hashed_password

        # Создаем пользователя
        new_user = self.model(**user_data_dict)
        self._session.add(new_user)
        await self._session.commit()
        await self._session.refresh(new_user)

        return {'message': 'Вы успешно зарегистрированы!'}

    async def authenticate_user(self, user_data: UserAuth) -> User:
        """Аутентифицировать пользователя."""
        user = await self.find_one_by_fields(email=user_data.email)
        if not user or not verify_password(user_data.password, user.password):
            raise IncorrectEmailOrPasswordException
        return user

    async def get_all_users(self) -> list[UserInfo]:
        """Получить информацию о всех пользователях."""
        users = await self.find_all()
        return [UserInfo.model_validate(user) for user in users]

    async def get_confidential_info(self, user: User) -> ConfidentialInfoResponse:
        '''Получить конфиденциальную информацию пользователя.'''
        return ConfidentialInfoResponse(email=user.email, password='******')
    
    # async def update_confidential_info(
    #     self,
    #     user: User,
    #     credentials: UpdateConfidentialInfoRequest
    # ) -> dict:
    #     '''Обновить конфиденциальную информацию пользователя.'''
    #     if user.email != credentials.email or not verify_password(credentials.password, user.password):
    #         raise HTTPException(status_code=400, detail='Неверный email или password!')
    
    #     if credentials.new_password != credentials.confirm_new_password:
    #         raise HTTPException(status_code=400, detail='Пароли не совпадают!')
    
    #     user.email = credentials.new_email
    #     user.password = get_password_hash(credentials.new_password)

    #     # Сессия уже передана в DAO, поэтому не нужно вызывать add()
    #     # self._session.add(user)

    #     await self._session.commit()
    
    #     return {'message': 'Конфиденциальные данные изменены успешно!'}