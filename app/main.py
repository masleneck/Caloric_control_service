from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from loguru import logger
from app.core.config import settings
from app.api.endpoints.auth import router as router_auth
from app.api.endpoints.nutrition import router as router_nutrition
from app.api.endpoints.questions import router as router_questions
from app.api.endpoints.profile import router as router_profile

# Инициализация Jinja2
templates = Jinja2Templates(directory='app/templates')

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
        allow_origins=['http://localhost:5500'],  # Укажите домен вашего фронтенда
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # Монтирование статических файлов
    app.mount(
        '/static',
        StaticFiles(directory='app/static'),
        name='static'
    )

    # Регистрация роутеров
    register_routers(app)
    return app


def register_routers(app: FastAPI) -> None:
    '''Регистрация роутеров приложения.'''
    # Корневой роутер
    root_router = APIRouter()

    @root_router.get('/', tags=['root'])
    async def index(request: Request):
        '''Рендеринг главной страницы'''
        return templates.TemplateResponse('index.html', {'request': request})
    
    # @root_router.get('/home')
    # async def show_home(request: Request):
    #     '''Отображает страницу home.html.'''
    #     return templates.TemplateResponse('home.html', {'request': request})

    # Подключение роутеров
    app.include_router(root_router)

    app.include_router(router_questions)
    app.include_router(router_auth)
    app.include_router(router_profile)
    app.include_router(router_nutrition)
    


# Создание экземпляра приложения
app = create_app()

# uvicorn app.main:app --port 8000 --reload  