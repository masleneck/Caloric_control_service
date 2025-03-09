from typing import List
from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.auth.utils import authenticate_user, set_tokens
from app.dependencies.auth_dep import get_current_user, get_current_admin_user, check_refresh_token
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.core.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.api.dao import UserDAO
from app.schemas.users import UserRegister, UserAuth, EmailModel, UserAddDB, UserInfo

router = APIRouter()


@router.post('/register/')
async def register_user(user_data: UserRegister,
                        session: AsyncSession = Depends(get_session_with_commit)) -> dict:
    # Проверка существования пользователя
    user_dao = UserDAO(session)

    existing_user = await user_dao.find_one_or_none(filters=EmailModel(email=user_data.email))
    if existing_user:
        raise UserAlreadyExistsException

    # Подготовка данных для добавления
    user_data_dict = user_data.model_dump()
    user_data_dict.pop('confirm_password', None)

    # Добавление пользователя
    await user_dao.add(values=UserAddDB(**user_data_dict))

    return {'message': 'Вы успешно зарегистрированы!'}


@router.post('/login/')
async def auth_user(
        response: Response,
        user_data: UserAuth,
        session: AsyncSession = Depends(get_session_without_commit)
) -> dict:
    users_dao = UserDAO(session)
    user = await users_dao.find_one_or_none(
        filters=EmailModel(email=user_data.email)
    )

    if not (user and await authenticate_user(user=user, password=user_data.password)):
        raise IncorrectEmailOrPasswordException
    set_tokens(response, user.id)
    return {
        'ok': True,
        'message': 'Авторизация успешна!'
    }


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('user_access_token')
    response.delete_cookie('user_refresh_token')
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get('/me/')
async def get_me(user_data: User = Depends(get_current_user)) -> UserInfo:
    return UserInfo.model_validate(user_data)


@router.get('/all_users/')
async def get_all_users(session: AsyncSession = Depends(get_session_with_commit),
                        user_data: User = Depends(get_current_admin_user)
                        ) -> List[UserInfo]:
    return await UserDAO(session).find_all()


@router.post('/refresh')
async def process_refresh_token(
        response: Response,
        user: User = Depends(check_refresh_token)
):
    set_tokens(response, user.id)
    return {'message': 'Токены успешно обновлены'}
