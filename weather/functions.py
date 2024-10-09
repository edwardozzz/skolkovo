import pandas as pd
from sqlalchemy.orm import sessionmaker
from models import WeatherData, engine

# Константы
PRESSURE_CONVERSION_FACTOR = 0.750062

# Функция для добавления данных о погоде в базу данных
def add_weather_data_to_db(weather_data):
    """
    Добавляет запись о погоде в базу данных.

    Аргумент:
        weather_data (dict): Словарь с данными о погоде.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Конвертируем давление из гПа в мм рт. ст.
        pressure_mmHg = weather_data.get('pressure_msl', 0) * PRESSURE_CONVERSION_FACTOR

        # Преобразуем направление ветра
        wind_direction = convert_wind_direction(weather_data.get('wind_direction_10m', 0))
        
        # Создаем запись данных о погоде
        weather_record = WeatherData(
            temperature=weather_data.get('temperature_2m', 0),
            wind_speed=weather_data.get('wind_speed_10m', 0),
            wind_direction=wind_direction,
            pressure=pressure_mmHg,
            precipitation=weather_data.get('precipitation', 0),
            timestamp=pd.to_datetime('now')  # Время записи
        )
        
        # Добавляем и коммитим запись
        session.add(weather_record)
        session.commit()
        print("Данные успешно добавлены в базу данных.")
    except Exception as e:
        print(f"Ошибка при добавлении данных в базу: {e}")
    finally:
        # Закрываем сессию для освобождения ресурсов
        session.close()

# Функция для преобразования углового направления ветра в строку
def convert_wind_direction(degrees):
    """
    Преобразует числовое направление ветра (в градусах) в строку.

    Аргумент:
        degrees (float): Числовое значение направления ветра в градусах.

    Возвращает:
        str: Строковое представление направления ветра (например, "С", "СВ").
    """
    directions = {
        0: "С", 45: "СВ", 90: "В", 135: "ЮВ", 180: "Ю", 225: "ЮЗ", 270: "З", 315: "СЗ"
    }
    # Находим ближайшее значение
    closest = min(directions.keys(), key=lambda x: abs(x - degrees))
    return directions[closest]
