import asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import TestQuestion, FoodItem
from app.core.database import async_session_maker
from loguru import logger
from app.core.food_data import REAL_FOOD_ITEMS  

async def init_test_questions(session: AsyncSession) -> None:
    '''Инициализация тестовых вопросов в базе данных'''
    try:
        # Удаляем старые вопросы
        await session.execute(delete(TestQuestion))
        await session.commit()
        # logger.info("Старые тестовые вопросы удалены!")
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
                text='Каков ваш текущий вес?',
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
                text='Есть ли у вас вредные привычки?',
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
        logger.success("Тестовые вопросы успешно инициализированы")

    except Exception as e:
        logger.error(f"Ошибка при инициализации тестовых вопросов: {e}")
        await session.rollback()
        raise


    

async def init_food_items(session: AsyncSession) -> None:
    try:
        await session.execute(delete(FoodItem))
        await session.commit()
        
        # Добавляем продукты партиями по 50 штук
        for i in range(0, len(REAL_FOOD_ITEMS), 50):
            batch = REAL_FOOD_ITEMS[i:i+50]
            food_items = [
                FoodItem(
                    name=item["name"],
                    calories=item["calories"],
                    proteins=item["proteins"],
                    fats=item["fats"],
                    carbs=item["carbs"]
                ) 
                for item in batch
            ]
            session.add_all(food_items)
            await session.commit()
            # logger.info(f"Добавлено {i+50 if i+50 < len(REAL_FOOD_ITEMS) else len(REAL_FOOD_ITEMS)} продуктов")
        
        logger.success(f"Всего добавлено {len(REAL_FOOD_ITEMS)} продуктов")
        
    except Exception as e:
        logger.error(f"Ошибка при добавлении продуктов: {e}")
        await session.rollback()
        raise



async def initialize_db_data():
    """Инициализация начальных данных в БД"""
    async with async_session_maker() as session:
        await init_test_questions(session)
        await init_food_items(session)

if __name__ == '__main__':
    asyncio.run(initialize_db_data())
    
# py -m app.core.db_init