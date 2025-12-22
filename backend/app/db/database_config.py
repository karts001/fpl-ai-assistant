from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.app.db.base import Base


class DatabaseConfig:
  """Configuration for database connection"""
  def __init__(self, db_url: str):
    self.engine = create_async_engine(
      url=db_url,
      echo=True,
      pool_pre_ping=True,
      pool_recycle=3600
    )
    self.AsyncSessionLocal = async_sessionmaker(
      autocommit=False,
      autoflush=False,
      class_=AsyncSession,
      expire_on_commit=False,
      bind=self.engine
    )

  async def create_all_tables(self) -> None:
    """Create all tables (useful for testin)"""
    async with self.engine.begin() as conn:
      await conn.run_sync(Base.metadata.drop_all)
      await conn.run_sync(Base.metadata.create_all)    