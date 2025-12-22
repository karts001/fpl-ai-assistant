from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database_config import DatabaseConfig


class BaseRepository:
  """Base repository with common database operations"""
  def __init__(self, db_config: DatabaseConfig):
    self.db_config = db_config

  @asynccontextmanager
  async def get_session(self) -> AsyncIterator[AsyncSession]:
    session: AsyncSession = self.db_config.AsyncSessionLocal()
    try:
      yield session
      session.commit()
    except SQLAlchemyError as e:
      session.rollback()
      raise e
    finally:
      session.close()