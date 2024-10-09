import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import datetime
import os

# Настройка подключения к базе данных
DATABASE_URL = "mysql+pymysql://root:123@localhost/weather_data"
engine = create_engine(DATABASE_URL)

# Функция для экспорта данных в Excel
def export_to_excel():
    """Экспортирует 10 последних записей из базы данных в файл .xlsx с автошириной столбцов."""
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Запрос для получения 10 последних записей, отсортированных по времени
        query = text("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 10")
        weather_records = session.execute(query).fetchall()

        # Преобразуем данные в DataFrame
        data = [{
            "ID": record.id,
            "Температура, °C": record.temperature,
            "Скорость ветра, м/с": record.wind_speed,
            "Направление ветра": record.wind_direction,
            "Давление, мм рт. ст": record.pressure,
            "Осадки, мм": record.precipitation,
            "Временная отметка": record.timestamp
        } for record in weather_records]
        df = pd.DataFrame(data)

        # Получаем текущую директорию проекта
        project_dir = os.path.dirname(os.path.abspath(__file__))

        # Генерируем имя файла с меткой времени
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weather_data_{timestamp}.xlsx"

        # Сохраняем файл в директории проекта
        file_path = os.path.join(project_dir, filename)
        df.to_excel(file_path, index=False, engine='openpyxl')

        # Открываем файл для настройки ширины столбцов
        from openpyxl import load_workbook
        workbook = load_workbook(file_path)
        worksheet = workbook.active

        # Устанавливаем автоширину для всех столбцов
        for column_cells in worksheet.columns:
            max_length = 0
            column = column_cells[0].column_letter  # Получаем букву столбца
            for cell in column_cells:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = max_length + 2
            worksheet.column_dimensions[column].width = adjusted_width

        # Сохраняем изменения
        workbook.save(file_path)

        print(f"Данные успешно экспортированы в файл {file_path}.")
    
    finally:
        session.close()

# Запуск функции экспорта
if __name__ == "__main__":
    export_to_excel()
