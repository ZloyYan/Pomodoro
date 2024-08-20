from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import Settings

settings = Settings()

# Connect to the SQLite database
engine = create_engine(settings.db_url)
Session = sessionmaker(engine) # sessionmaker является фабричным классом из библиотеки SQLAlchemy, который создает новые сессии для взаимодействия с базой данных. В данном контексте, Session является объектом, который создается с помощью sessionmaker.

def get_db_session() -> Session: # Функция для получения сессии базы данных. -> Session - указывает, что возвращается объект сессии базы данных. Смысловой нагрузки не несёт, но говорит о том, что функция вернёт объект класса Session.
    return Session()
