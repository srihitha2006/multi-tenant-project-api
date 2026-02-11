import asyncio
import app.db.models
from app.db.base import Base
from app.db.session import engine  # ✅ engine is here

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
