from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger
from app.core.config import settings
from app.api.routers import main_router 

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
        description='API для управления пользователями, тренировками и их питанием',
        lifespan=lifespan,
    )
    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],  # Разрешаем все источники
        allow_credentials=True,
        allow_methods=['*'], # Разрешаем все методы
        allow_headers=['*'], # Разрешаем все заголовки
    )
    # Монтирование статических файлов
    app.mount(
        "/static",
        StaticFiles(directory="app/static"),
        name="static"
    )
    # Регистрация роутеров
    app.include_router(main_router)
    return app