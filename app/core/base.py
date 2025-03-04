'''
Этот файл будет содержать базовый класс Base, который используется во всех моделях.

Файл содержит модели, которые представляют таблицы базы данных. SQLAlchemy автоматически создает их на основе этих классов
'''
from app.core.db import Base #noqa
from app.models import food_items, meals, test_questions, test_results, users, workouts

