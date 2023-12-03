import os
from atexit import (
    register,
)  # можно передать функцию для выполнения при закрытии приложения
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, func


PG_USER = os.getenv("PG_USER", "user")
PG_PASSWORD = os.getenv("PG_PASSWORD", "1234")
PG_DB = os.getenv("PG_DB", "testapp")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv(
    "PG_PORT", 5431
)  # 5432 - для локальной БД, 5431 - для БД в docker-compose

PG_DSN = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_engine(PG_DSN)

# функция которая при завершении работы с приложением закрое соединение с БД
register(engine.dispose)

# создание сессии с использованием движка
Session = sessionmaker(bind=engine)
# создание базового класса для модели
Base = declarative_base(bind=engine)

"""API для управления объявлениями"""


class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String)
    author = Column(String, nullable=False)
    creation_time = Column(
        DateTime, server_default=func.now()
    )  # func позволяет выполнить процедуру на стороне сервера БД
   


# Выполнение миграции
Base.metadata.create_all()
