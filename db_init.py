import asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.test_questions import TestQuestion
from app.dao.db import async_session_maker

async def add_test_questions():
    '''Удаляет старые вопросы и добавляет новые'''
    async with async_session_maker() as session:
        # Удаляем старые вопросы
        await session.execute(delete(TestQuestion))
        await session.commit()

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
                options=None
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
                text='Вредные привычки:',
                type='options',
                options=['Их нет', 'Люблю Амаля', 'HQD-монстр', 'Наркоман', 'Алкоголик']
            ),
        ]

        session.add_all(questions)
        await session.commit()
        print('Вопросы успешно обновлены в БД!')

if __name__ == '__main__':
    asyncio.run(add_test_questions())

# py -m db_init