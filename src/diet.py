
def calculate_daily_calories(age, height, current_weight, desired_weight, sex):
    # Расчет BMR в зависимости от пола
    if sex.lower() == "male":
        bmr = 10 * current_weight + 6.25 * height - 5 * age + 5
    elif sex.lower() == "female":
        bmr = 10 * current_weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Пол должен быть 'male' или 'female'")

    # Множитель активности
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "high": 1.725,
        "very_high": 1.9
    }


    daily_calories = bmr * activity_multipliers["light"]

    # План по калориям для достижения желаемого веса
    if desired_weight < current_weight:
        target_calories = daily_calories - 500  # Для похудения (примерный дефицит 500 ккал/день)
    elif desired_weight > current_weight:
        target_calories = daily_calories + 500  # Для набора массы (примерный профицит 500 ккал/день)
    else:
        target_calories = daily_calories  # Для поддержания текущего веса

    return {
        "bmr": bmr,
        "daily_calories": daily_calories,
        "target_calories": target_calories
    }

