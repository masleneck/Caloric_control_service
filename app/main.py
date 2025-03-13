from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from typing import Optional
from app.core.config import settings
from app.auth.router import router as router_auth
from app.api.endpoints.nutrition import router as router_nutrition



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    '''Управление жизненным циклом приложения.'''
    logger.info('Инициализация приложения...')
    yield
    logger.info('Завершение работы приложения...')


def create_app() -> FastAPI:
    '''
   Создание и конфигурация FastAPI приложения.
   Returns: Сконфигурированное приложение FastAPI
   '''
    app = FastAPI(
        title=settings.APP_TITLE,
        description=('API для управления пользователями, тренировками и их питанием'),
    )
    # Монтирование статических файлов
    app.mount(
        '/static',
        StaticFiles(directory='app/static'),
        name='static'
    )
    templates = Jinja2Templates(directory='app/templates')
    # Регистрация роутеров
    register_routers(app)
    return app


def register_routers(app: FastAPI) -> None:
    '''Регистрация роутеров приложения.'''
    # Корневой роутер
    root_router = APIRouter()

    @root_router.get('/', tags=['root'])
    def home_page():
        return {'hello!!!'}

    # Подключение роутеров

    app.include_router(root_router, tags=['root'])
    app.include_router(router_auth)
    
    app.include_router(router_nutrition)




# Создание экземпляра приложения
app = create_app()
