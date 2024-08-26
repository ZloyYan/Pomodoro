from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from settings import Settings

settings = Settings()

# Connect to the SQLite database
engine = create_async_engine(url=settings.db_url, future=True, echo=True, pool_pre_ping=True)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expired_on_commit=False,
)
# Заменили это на async_sessionmaker, чтобы использовать асинхронные сессии
# Session = sessionmaker(engine) # sessionmaker является фабричным классом из библиотеки SQLAlchemy, который создает новые сессии для взаимодействия с базой данных. В данном контексте, Session является объектом, который создается с помощью sessionmaker.

async def get_db_session() -> AsyncSession: # Функция для получения сессии базы данных. -> Session - указывает, что возвращается объект сессии базы данных. Смысловой нагрузки не несёт, но говорит о том, что функция вернёт объект класса Session.
    async with AsyncSessionFactory() as session:
        yield session
