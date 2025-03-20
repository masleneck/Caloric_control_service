from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from loguru import logger

# Инициализация Jinja2
templates = Jinja2Templates(directory='app/templates')

router = APIRouter(
    tags=['Страницы 📄']
)

@router.get('/', summary='root')
async def index(request: Request):
    '''Рендеринг главной страницы'''
    logger.info('Вызван маршрут /')
    return templates.TemplateResponse('index.html', {'request': request})
    
@router.get('/home', summary='home')
async def show_home(request: Request):
    '''Отображает страницу home.html.'''
    logger.info('Вызван маршрут /home')
    return templates.TemplateResponse('home.html', {'request': request})
    

@router.get('/quiz', summary='quiz')
async def show_quiz(request: Request):
    '''Отображает страницу quiz.html.'''
    logger.info('Вызван маршрут /quiz')
    return templates.TemplateResponse('quiz.html', {'request': request})