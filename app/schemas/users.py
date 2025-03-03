'''
✅Схемы данных (Pydantic)
Файл нужен для проверки данных, которые приходят в API, и для определения формата ответа

🟢BaseModel - базовый класс Pydantic, от которого мы наследуем схемы
🟢EmailStr - специальный тип данных, который проверяет, что строка является email-адресом
🟢Field - позволяет задавать ограничения для полей (например, макс. длина строки)
'''
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator
from datetime import date
from typing import Optional

from app.models.users import UserRole, Gender, ActivityLevel


class UserResponse(BaseModel): # определяет, какие данные API возвращает в ответе
    '''
    Схема для ответа API
    '''
    id: int # идентификатор пользователя
    name: str # имя пользователя
    email: str # email пользователя
    username: str
    birthday_date: Optional[date] = None
    weight: Optional[float] = None  
    height: Optional[int] = None  
    gender: Optional[Gender] = None  
    activity_level: Optional[ActivityLevel] = None  
    role: UserRole  


    model_config = ConfigDict(from_attributes=True)  

     # позволяет передавать объекты SQLAlchemy в response_model
#  Без from_attributes = True FastAPI не сможет автоматически преобразовать объект SQLAlchemy в JSON



class UserCreate(BaseModel): # проверяет данные при создании пользователя
    '''
    Схема для создания пользователя
    '''
    name: str = Field(min_length=2, max_length=30, example='Андрей')  # Ограничение длины имени
    email: EmailStr = Field(example='user@example.com')  # Встроенная проверка email
    username: str = Field(min_length=3, max_length=20, example='andrey123')
    password: str = Field(min_length=6, max_length=50, example='securepassword_123')  # Минимальная длина пароля
    birthday_date: Optional[date] = None
    weight: Optional[float] = Field(ge=30, le=300, example=75.5)  # Вес от 30 до 300 кг
    height: Optional[int] = Field(ge=100, le=250, example=180)  # Рост от 100 до 250 см
    gender: Optional[Gender] = None  
    activity_level: Optional[ActivityLevel] = None  

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after') # after, что означает, что они выполняются после валидации отдельных полей.
    def check_age(self):
        today = date.today()
        age = today.year - self.birthday_date.year - (
            (today.month, today.day) < (self.birthday_date.month, self.birthday_date.day))

        if age <= 0:
            raise ValueError('Введите корректный возраст!')
        if age > 120:
            raise ValueError('Возраст не может превышать 120 лет')
        return self


class UserUpdate(BaseModel):
    '''Схема для обновления данных пользователя.'''
    name: Optional[str] = Field(min_length=3, max_length=20, example='new_name')
    email: Optional[EmailStr] = Field(example='new_email@example.com')
    password: Optional[str] = Field(min_length=6, max_length=50, example='new_secure_password')
    weight: Optional[float] = Field(ge=30, le=300, example=80.0)  
    height: Optional[int] = Field(ge=100, le=250, example=175)  
    gender: Optional[Gender] = None  
    activity_level: Optional[ActivityLevel] = None  

    model_config = ConfigDict(from_attributes=True) 


class UserUpdateAdmin(BaseModel):
    '''Расширенная схема для обновления данных пользователя (админ).'''
    goal_id: Optional[int] = None 
    name: Optional[str] = Field(min_length=2, max_length=30, example='admin')
    email: Optional[EmailStr] = Field(example='admin@example.com')
    username: Optional[str] = Field(min_length=3, max_length=20, example='admin_user')
    password: Optional[str] = Field(min_length=6, max_length=50, example='admin_password')
    birthday_date: Optional[date] = None
    role: Optional[UserRole]   
    weight: Optional[float] = Field(None, ge=30, le=300, example=80.0) 
    height: Optional[int] = Field(None, ge=100, le=250, example=175)  
    gender: Optional[Gender] = None  
    activity_level: Optional[ActivityLevel] = None 
     
    model_config = ConfigDict(from_attributes=True)