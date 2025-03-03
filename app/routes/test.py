from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.db import get_async_session
from app.models.test_questions import TestQuestion


router = APIRouter()


templates = Jinja2Templates(directory='app/templates')


@router.get('/')
async def index_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/test')
async def get_test_questions(session: AsyncSession = Depends(get_async_session)): 
    questions = await session.execute(select(TestQuestion))
    questions_list = questions.scalars().all()

    result = []
    for question in questions_list:
        question_data = {
            'id': question.id,
            'text': question.text,
            'type': 'options' if 'options' in question.type else 'input',
            'options': question.options if question.options else None
        }
        result.append(question_data)
        
    return result

