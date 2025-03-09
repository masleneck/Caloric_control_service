import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.models.test_questions import TestQuestion
from app.dao.db import get_async_session

async def add_test_questions():
    '''Удаляем старые вопросы и добавляем новые'''
    async for db in get_async_session():  
        # Удаляем все старые вопросы
        await db.execute(delete(TestQuestion))
        await db.commit()
        
        # Добавляем новые вопросы
        questions = [
            TestQuestion(
                text='Как часто вы занимаетесь спортом?',
                type='options',
                options=['Не занимаюсь', 'Редко', 'Два раза в неделю', 'Каждый день', 'Спортсмен']
            ),
            TestQuestion(
                text='Сколько литров воды Вы пьете в день:',
                type='input',
                options=None  # Для input-полей options нет
            ),
            TestQuestion(
                text='Сколько часов Вы спите в сутки?',
                type='options',
                options=['Менее 5', '5-6', '7-8', 'Более 8']
            ),
            TestQuestion(
                text='Ваш вес (кг):',
                type='input',
                options=None
            ),
            TestQuestion(
                text='Ваш уровень активности:',
                type='options',
                options=['На чиле', 'Лёгкая активность', 'Средняя активность', 'Высокая активность', 'Чемпик']
            ),
            TestQuestion(
                text='Есть ли у вас вредные привычки?:',
                type='options',
                options=['Я алкаш', 'HQD-монстр', 'Люблю Амаля']
            ),
        ]
        
        db.add_all(questions)
        await db.commit()
        print('Вопросы успешно обновлены в БД!')
        break  

if __name__ == '__main__':
    asyncio.run(add_test_questions())

# PS C:\fastapi_project> py -m app.core.db_init