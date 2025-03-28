from settings import DB_URL
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker


class Database:
    # handles database engine and session lifecycle
    def __init__(self):
        self.engine: AsyncEngine = create_async_engine(DB_URL, echo=True)
        self.session_factory = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_session(self):
        async with self.session_factory() as session:
            yield session
