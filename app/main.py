from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.routes import users, workouts, auth, food_items, meals, test, test_questions, goals

app = FastAPI(
    title=settings.app_title,  
    description='API для управления пользователями и тренировками',
)

app.mount('/static', StaticFiles(directory='app/static'), name='static')

templates = Jinja2Templates(directory='app/templates')

app.include_router(test.router)

app.include_router(workouts.router)
app.include_router(auth.router)  
app.include_router(users.router)
app.include_router(food_items.router)
app.include_router(meals.router)
app.include_router(goals.router)
app.include_router(test_questions.router)


if __name__ == '__main__':
    pass
    # import os
    # import uvicorn
    
    # print(os.path.exists('templates/index.html')) 
    # print(os.path.exists('static')) 

    # print(os.environ.get('DATABASE_URL'))
    # print(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

    # uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)

    # uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
    