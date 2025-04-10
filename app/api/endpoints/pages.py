from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, HTTPException
from loguru import logger
from pathlib import Path

# Инициализация Jinja2
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    tags=['Страницы 📄']
)

def check_template_exists(template_name: str) -> None:
    """Проверяет существование шаблона"""
    template_path = Path(f"app/templates/{template_name}")
    if not template_path.exists():
        logger.error(f"Шаблон {template_name} не найден")
        raise HTTPException(404, detail=f"Template {template_name} not found")

@router.get('/', summary='root', response_class=HTMLResponse)
async def index(request: Request):
    logger.info('Вызван маршрут /')
    check_template_exists('index.html')
    return templates.TemplateResponse('index.html', {'request': request})
    
@router.get('/home', summary='home', response_class=HTMLResponse)
async def show_home(request: Request):
    logger.info('Вызван маршрут /home')
    check_template_exists('home.html')
    return templates.TemplateResponse('home.html', {'request': request})
    
@router.get('/quiz', summary='quiz', response_class=HTMLResponse)
async def show_quiz(request: Request):
    logger.info('Вызван маршрут /quiz')
    check_template_exists('quiz.html')
    return templates.TemplateResponse('quiz.html', {'request': request})

@router.get('/profile', summary='profile', response_class=HTMLResponse)
async def show_profile(request: Request):
    logger.info('Вызван маршрут /profile')
    check_template_exists('profile.html')
    return templates.TemplateResponse('profile.html', {'request': request})