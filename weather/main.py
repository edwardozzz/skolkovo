import asyncio
import httpx
from functions import add_weather_data_to_db, convert_wind_direction


# Асинхронная функция для получения данных о погоде
async def fetch_weather():
    """
    Асинхронно запрашивает данные о погоде и сохраняет их в базу данных каждые 3 минуты.
    """
    latitude = 55.697698  # Широта
    longitude = 37.359713  # Долгота
    api_url = (
        f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}'
        '&current=temperature_2m,wind_direction_10m,wind_speed_10m,pressure_msl,precipitation&timezone=auto'
    )

    async with httpx.AsyncClient() as client:
        while True:
            try:
                # Получаем данные с API
                response = await client.get(api_url)
                response.raise_for_status()  # Проверка успешности запроса
                weather_data = response.json()

                # Извлекаем данные о погоде
                current_data = weather_data.get('current', {})
                
                # Сохраняем данные в базу данных
                add_weather_data_to_db(current_data)

                # Ждем 3 минуты перед следующим запросом
                await asyncio.sleep(180)

            except Exception as e:
                print(f"Ошибка при запросе данных: {e}")
                await asyncio.sleep(30)  # Пауза перед повторным запросом в случае ошибки


# Главная функция
async def main():
    """
    Основная функция для запуска асинхронного процесса сбора данных о погоде.
    """
    # Создаем задачу для получения данных о погоде
    fetch_task = asyncio.create_task(fetch_weather())
    await fetch_task  # Ожидаем завершения задачи


# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
