import asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.test_questions import TestQuestion
from app.core.database import async_session_maker

async def add_test_questions():
    '''Удаляет старые вопросы и добавляет новые'''
    async with async_session_maker() as session:
        # Удаляем старые вопросы
        await session.execute(delete(TestQuestion))
        await session.commit()

        # Добавляем новые вопросы
        questions = [
            TestQuestion(
                name='gender',
                text='Ваш пол?',
                type='options',
                options=['Мужской', 'Женский']  # MALE, FEMALE
            ),
            TestQuestion(
                name='birthday_date',
                text='Дата вашего рождения?',
                type='input',
                options=None  # '2003-05-22'
            ),
            TestQuestion(
                name='height',
                text='Каков ваш рост?',
                type='input',
                options=None  # 168
            ),
            TestQuestion(
                name='weight',
                text='Каков ваш текущий вес(кг)?',
                type='input',
                options=None  # 52
            ),
            TestQuestion(
                name='goal',
                text='Выбери свою цель',
                type='options',
                options=['Снизить вес', 'Поддержание формы', 'Набрать мышечную массу']  # LOSE_WEIGHT, KEEPING_FIT, GAIN_MUSCLE_MASS
            ),
            TestQuestion(
                name='bad_habits',
                text='Есть ли у вас вредные привычки ?',
                type='options',
                options=['Да', 'Нет']
            ),
            TestQuestion(
                name='steps_per_day',
                text='Сколько вы примерно проходите шагов за день?',
                type='input',
                options=None  # 5000
            ),
            TestQuestion(
                name='sleep_hours',
                text='Сколько часов вы в среднем спите в день?',
                type='input',
                options=None  # 7
            ),
            TestQuestion(
                name='water_intake',
                text='Сколько воды вы в среднем пьете в день?',
                type='options',
                options=['Менее 0,5л', '0,5-1,5л', '1.5-3л', 'Более 3л']  # менее 2 стаканов и т.п.
            ),
            TestQuestion(
                name='hormone_issues',
                text='Есть ли у вас гормональные нарушения?',
                type='options',
                options=[
                    'Нет / Никогда не сдавал анализы',
                    'Гипотиреоз',
                    'Лептинорезистентность/Инсулинорезистентность',
                    'Дефициты половых гормонов и различные активные компенсаторные механизмы',
                    'Различные эндокринные нарушения'
                ]
            )
        ]

        session.add_all(questions)
        await session.commit()
        print('Вопросы успешно обновлены в БД!')

if __name__ == '__main__':
    asyncio.run(add_test_questions())
    
# py -m db_init