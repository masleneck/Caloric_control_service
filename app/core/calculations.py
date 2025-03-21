from datetime import date

def calculate_metrics(data: dict):
    '''Расчёт калорий, БЖУ и ИМТ'''
    gender = data['gender']
    birthday_date = data['birthday_date']
    height = data['height']
    weight = data['weight']
    goal = data['goal']
    bad_habits = data['bad_habits']
    steps_per_day = data['steps_per_day']
    sleep_hours = data['sleep_hours']
    water_intake = data['water_intake']
    hormone_issues = data['hormone_issues']

    # Возраст
    age = date.today().year - birthday_date.year

    # BMR по Миффлину-Сан Жеору
    bmr = (10 * weight + 6.25 * height - 5 * age + (5 if gender == 'MALE' else -161))

    # Коэффициент активности
    activity_factor = (
        1.2 if steps_per_day < 5000 else 
        1.375 if steps_per_day < 10000 else 
        1.55
    )

    # Корректировка на цель
    goal_factors = {'LOSE_WEIGHT': 0.9, 'GAIN_MUSCLE_MASS': 1.1}
    activity_factor *= goal_factors.get(goal, 1.0)

    # Корректировки на вредные привычки, сон, воду, гормоны
    if bad_habits == 'Да':
        activity_factor *= 0.95
    if sleep_hours < 6:
        activity_factor *= 0.95
    elif sleep_hours > 8:
        activity_factor *= 1.05

    water_factors = {'Менее 0,5л': 0.95, '0,5-1,5л': 0.98, '1.5-3': 1.0, 'Более 3л': 1.05}
    activity_factor *= water_factors.get(water_intake, 1.0)

    hormone_factors = {
        'Гипотиреоз': 0.9,
        'Лептинорезистентность/Инсулинорезистентность': 0.95,
        'Дефициты половых гормонов': 0.9,
        'Различные эндокринные нарушения': 0.85
    }
    activity_factor *= hormone_factors.get(hormone_issues, 1.0)

    # Финальный расчёт калорийности
    tdee = round(bmr * activity_factor, 1)

    # Эффективный вес (по формуле Девина)
    height_inches = height / 2.54
    effective_weight = round((50 if gender == 'MALE' else 45.5) + 2.3 * (height_inches - 60), 2)

    # Макронутриенты
    protein = round(1.8 * weight, 1)
    fat = round(1.0 * weight, 1)
    carbs = round((tdee - (protein * 4 + fat * 9)) / 4, 1)

    # Индекс массы тела
    bmi = round(weight / ((height / 100) ** 2), 1)

    # Рекомендации по воде
    recommended_water = round(weight * 0.035, 1)

    return {
        'Калорийность': tdee,
        'Белки (г)': protein,
        'Жиры (г)': fat,
        'Углеводы (г)': carbs,
        'Эффективный вес': effective_weight,
        'ИМТ': bmi,
        'Рекомендуемое потребление воды (л)': recommended_water
    }
