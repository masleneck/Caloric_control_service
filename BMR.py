from typing import Literal

def recommend_workout(
    age: int,
    weight: float,
    goal: Literal["lose", "maintain", "gain"],
    activity_level: float,
    habits: list[str]
) -> dict:
    """
    Подбирает программу тренировок на основе данных пользователя.
    
    :param age: Возраст (лет)
    :param weight: Вес (кг)
    :param goal: Цель ("lose" - похудение, "maintain" - поддержание, "gain" - набор массы)
    :param activity_level: Уровень активности (1.2 - 1.9)
    :param habits: Список вредных привычек (["smoking", "alcohol"])
    :return: Словарь с рекомендациями по тренировкам
    """

    workout_plan = {
        "type": None,         # Тип тренировок
        "frequency": None,    # Частота (раз в неделю)
        "duration": None,     # Длительность (минуты)
        "intensity": None     # Интенсивность (низкая/средняя/высокая)
    }

    # 1. Определяем тип тренировок
    if goal == "lose":
        workout_plan["type"] = "Кардио + Силовые"
    elif goal == "gain":
        workout_plan["type"] = "Силовые + Высокоинтенсивные"
    else:
        workout_plan["type"] = "Смешанные (силовые + кардио)"

    # 2. Определяем частоту тренировок
    if activity_level < 1.4:  # Малоподвижный образ жизни
        workout_plan["frequency"] = 3
    elif activity_level < 1.7:
        workout_plan["frequency"] = 4
    else:
        workout_plan["frequency"] = 5

    # 3. Корректируем длительность
    if age < 30:
        workout_plan["duration"] = 60
    elif age < 50:
        workout_plan["duration"] = 45
    else:
        workout_plan["duration"] = 35  # Уменьшаем нагрузку

    # 4. Определяем интенсивность
    if goal == "lose":
        workout_plan["intensity"] = "Высокая"
    elif goal == "gain":
        workout_plan["intensity"] = "Средняя"
    else:
        workout_plan["intensity"] = "Низкая"

    # 5. Коррекция по привычкам
    if "smoking" in habits or "alcohol" in habits:
        workout_plan["intensity"] = "Средняя"  # Уменьшаем нагрузку
        workout_plan["duration"] -= 5  # Убираем 5 минут

    return workout_plan



if __name__ == '__main__':    
    workout = recommend_workout(
        age=28,
        weight=75,
        goal="lose",
        activity_level=1.6,
        habits=["alcohol"]
        )
    print(workout)
