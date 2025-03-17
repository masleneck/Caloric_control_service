from datetime import datetime, date
from typing import Self
from pydantic import (
    BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator, computed_field
)
from app.utils.auth_utils import get_password_hash
from app.models.users import Role
from app.models.profiles import Gender, CurrentGoal, ActivityLevel


class EmailModel(BaseModel):
    '''Базовая модель для хранения электронной почты.'''
    email: EmailStr = Field(description='Электронная почта')
    model_config = ConfigDict(from_attributes=True)


class UserBase(EmailModel):
    '''Базовая модель пользователя.'''
    model_config = ConfigDict(from_attributes=True)


class UserRegister(UserBase):
    '''Модель для регистрации пользователя.'''
    password: str = Field(min_length=5, max_length=50, description='Пароль, от 5 до 50 знаков')
    confirm_password: str = Field(min_length=5, max_length=50, description='Повторите пароль')

    @model_validator(mode='after')
    def check_password(self) -> Self:
        '''Проверяет совпадение паролей и хеширует их перед сохранением.'''
        if self.password != self.confirm_password:
            raise ValueError('Пароли не совпадают')
        self.password = get_password_hash(self.password)
        return self


class UserAuth(EmailModel):
    '''Модель для авторизации пользователя.'''
    password: str = Field(min_length=5, max_length=50, description='Пароль, от 5 до 50 знаков')


class UserAddDB(UserBase):
    '''Модель для хранения данных пользователя в базе данных.'''
    password: str = Field(min_length=5, description='Пароль в формате HASH-строки')


class ProfileModel(BaseModel):
    '''Модель профиля пользователя.'''
    user_id: int = Field(description='Идентификатор пользователя')
    name: str = Field(min_length=3, max_length=50, description='Имя, от 3 до 50 символов')
    last_name: str | None = Field(None, min_length=3, max_length=50, description='Фамилия, от 3 до 50 символов')
    gender: Gender = Field(default=Gender.NOT_STATED, description='Пол пользователя')
    weight: float = Field(gt=0, description='Вес пользователя в кг')
    height: int = Field(gt=0, description='Рост пользователя в см')
    goal: CurrentGoal = Field(default=CurrentGoal.NOT_STATED, description='Цель пользователя')
    birthday_date: datetime | None = Field(None, description='Дата рождения')
    activity_level: ActivityLevel = Field(default=ActivityLevel.NOT_STATED, description='Уровень активности')

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserInfo(UserBase):
    '''Расширенная модель информации о пользователе.'''
    id: int = Field(description='Идентификатор пользователя')
    role: Role = Field(description='Роль пользователя', exclude=True)
    profile: ProfileModel | None = Field(description='Профиль пользователя', exclude=True)

    @computed_field
    def role_name(self) -> str:
        '''Возвращает название роли.'''
        return self.role.value  # так как Role — это Enum, используем `.value`


class ConfidentialInfoResponse(BaseModel):
    email: str
    password: str

class UpdateConfidentialInfoRequest(BaseModel):
    email: str
    password: str
    new_email: str
    new_password: str
    confirm_new_password: str