from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Connect to the SQLite database
DATABASE_URL = "postgresql+psycopg2://postgres:password@0.0.0.0:5432/pomodoro" # Замените на св
engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine) # sessionmaker является фабричным классом из библиотеки SQLAlchemy, который создает новые сессии для взаимодействия с базой данных. В данном контексте, Session является объектом, который создается с помощью sessionmaker.

def get_db_session() -> Session: # Функция для получения сессии базы данных. -> Session - указывает, что возвращается объект сессии базы данных. Смысловой нагрузки не несёт, но говорит о том, что функция вернёт объект класса Session.
    return Session()