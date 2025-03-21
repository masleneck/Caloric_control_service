import asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.test_questions import TestQuestion
from app.data.db import async_session_maker

async def add_test_questions():
    '''Удаляет старые вопросы и добавляет новые'''
    async with async_session_maker() as session:
        # Удаляем старые вопросы
        await session.execute(delete(TestQuestion))
        await session.commit()

        # Добавляем новые вопросы
        questions = [
            TestQuestion(
                text='Ваш пол?',
                type='options',
                options=['Мужской', 'Женский'] # MALE, FEMALE
            ),
            TestQuestion(
                text='Дата вашего рождения?',
                type='input',
                options=None # '2003-05-22'
            ),
            TestQuestion(
                text='Каков ваш рост?',
                type='input',
                options=None # 168
            ),
            TestQuestion(
                text='Каков ваш текущий вес(кг)?',
                type='input',
                options=None # 52
            ),
            TestQuestion(
                text='Выбери свою цель',
                type='options',
                options=['Снизить вес', 'Поддержание формы', 'Набрать мышечную массу'] # LOSE_WEIGHT,KEEPING_FIT,GAIN_MUSCLE_MASS
            ),
            TestQuestion(
                text='Есть ли у вас вредные привычки ?',
                type='options',
                options=['Да','Нет']
            ),
            TestQuestion(
                text='Сколько вы примерно проходите шагов за день?',
                type='input',
                options=None # 5000
            ),
            TestQuestion(
                text='Сколько часов вы в среднем спите в день?',
                type='input',
                options=None # 7
            ),
            TestQuestion(
                text='Сколько воды вы в среднем пьете в день?',
                type='options',
                options=['Менее 0,5л','0,5-1,5л','1.5-3л','Более 3л'] # менее 2стаканов; 2-6стаканов; 7-12 стаканов; Более 12
            ),
            TestQuestion(
                text='Есть ли у вас гормональные нарушения?',
                type='options',
                options=['Нет / Никогда не сдавал анализы',
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