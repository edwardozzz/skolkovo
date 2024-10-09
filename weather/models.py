from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base

# Настройка подключения к базе данных
DATABASE_URL = "mysql+pymysql://root:123@localhost/weather_data"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Определение модели данных
class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String(10))
    pressure = Column(Float)
    precipitation = Column(Float)
    timestamp = Column(DateTime)

# Создание таблицы в базе данных (если она еще не существует)
Base.metadata.create_all(engine)
print("Таблица 'weather_data' успешно создана в базе данных.")
