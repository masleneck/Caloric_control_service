from datetime import datetime
from typing import Self
from pydantic import (
    BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator, computed_field
)
from app.models.users import Role
from app.models.profiles import Gender, CurrentGoal, ActivityLevel


class EmailModel(BaseModel):
    '''Базовая модель для хранения электронной почты.'''
    email: EmailStr 
    model_config = ConfigDict(from_attributes=True)


class UserBase(EmailModel):
    '''Базовая модель пользователя.'''
    model_config = ConfigDict(from_attributes=True)


class UserRegister(UserBase):
    '''Модель для регистрации пользователя.'''
    password: str = Field(min_length=5, max_length=50)
    confirm_password: str = Field(min_length=5, max_length=50)
    fullname: str = Field(min_length=3, max_length=101)
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        'example': {
            'email': 'Введите валидный email',
            'password': 'Пароль, от 5 до 50 знаков',
            'confirm_password': 'Повторите пароль',
            'fullname': 'Полное имя (имя и фамилия через пробел)'
        }
    })

    @model_validator(mode='after')
    def check_password(self) -> Self:
        '''Проверяет совпадение паролей.'''
        if self.password != self.confirm_password:
            raise ValueError('Пароли не совпадают')
        return self
    
    @property
    def name(self) -> str:
        '''Извлекает имя из fullname.'''
        return self.fullname.split()[0]

    @property
    def last_name(self) -> str | None:
        '''Извлекает фамилию из fullname.'''
        parts = self.fullname.split()
        return parts[1] if len(parts) > 1 else None


class UserAuth(EmailModel):
    '''Модель для авторизации пользователя.'''
    password: str
    model_config = ConfigDict(from_attributes=True)

class UserAddDB(UserBase):
    '''Модель для хранения данных пользователя в базе данных.'''
    password: str
    model_config = ConfigDict(from_attributes=True)

class ProfileModel(BaseModel):
    '''Модель профиля пользователя.'''
    user_id: int
    name: str 
    last_name: str | None 
    gender: Gender 
    weight: float
    height: int 
    goal: CurrentGoal 
    birthday_date: datetime | None 
    activity_level: ActivityLevel
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserInfo(UserBase):
    '''Расширенная модель информации о пользователе.'''
    id: int 
    role: Role
    profile: ProfileModel | None 
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    @computed_field
    def role_name(self) -> str:
        '''Возвращает название роли.'''
        return self.role.value  # так как Role — это Enum, используем `.value`


class ConfidentialInfoResponse(BaseModel):
    email: str
    password: str
    model_config = ConfigDict(from_attributes=True)

class UpdateConfidentialInfoRequest(BaseModel):
    email: str
    password: str
    new_email: str
    new_password: str
    confirm_new_password: str
    model_config = ConfigDict(from_attributes=True)