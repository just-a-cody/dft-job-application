from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(url="postgresql+asyncpg://admin:password@localhost:5432/fastapi", echo=True)
Base = declarative_base()
Session = async_sessionmaker(bind=engine)


# Add dependency to get session
async def get_session():
    async with Session() as sess:
        try:
            yield sess
        finally:
            await sess.close()
