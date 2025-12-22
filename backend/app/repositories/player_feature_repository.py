from typing import List, Optional

from sqlalchemy import desc, select

from backend.app.models.ml.player_feature_snapshot import PlayerFeatureSnapshot
from backend.app.db.database_config import DatabaseConfig
from backend.app.repositories.base_repository import BaseRepository


class PlayerFeatureRepository(BaseRepository):  
  def __init__(self, db_config: DatabaseConfig):
    super().__init__(db_config)

  async def bulk_insert(self, snapshots: List[PlayerFeatureSnapshot]) -> int:

    if not snapshots:
      return 0
    
    async with self.get_session() as session:
      db_snapshots = [
        PlayerFeatureSnapshot(**snap.model_dump())
        for snap in snapshots
      ]

      session.add_all(db_snapshots)
      return len(db_snapshots)
    
  async def get_by_gameweek(self, gameweek: int) -> List[PlayerFeatureSnapshot]:
    async with self.get_session() as session:
      stmt = select(PlayerFeatureSnapshot).where(
        PlayerFeatureSnapshot.gameweek == gameweek
      )

      result = await session.execute(stmt)

      return list(result.scalars().all())
    
  async def get_by_gameweek_range(self, start_gw: int, end_gw: int) -> List[PlayerFeatureSnapshot]:
    async with self.get_session() as session:
      stmt = (select(PlayerFeatureSnapshot)
        .where(PlayerFeatureSnapshot.gameweek >= start_gw)
        .where(PlayerFeatureSnapshot <= end_gw)
      )

      result = await session.execute(stmt)
      
      return list(result.scalars().all())

  async def get_by_player_and_gameweek(self, player_id: int, gameweek: int) -> List[PlayerFeatureSnapshot]:
    async with self.get_session() as session:
      stmt = (select(PlayerFeatureSnapshot)
        .where(PlayerFeatureSnapshot.player_id == player_id)
        .where(PlayerFeatureSnapshot.gameweek == gameweek)
      )

      result = await session.execute(stmt)
      
      return list(result.scalars().all())
  
  async def get_latest_by_player(self, player_id: int, limit: int = 10):
    async with self.get_session() as session:
      stmt = (select(PlayerFeatureSnapshot)
        .where(PlayerFeatureSnapshot.player_id == player_id)
        .order_by(desc(PlayerFeatureSnapshot.snapshot_time))
        .limit(limit)
      )
      
      result = await session.execute(stmt)
      
      return list(result.scalars().all())
    
  async def get_training_data(self, 
    start_gw: int, 
    end_gw: int, 
    team_name: Optional[str] = None
  ) -> List[PlayerFeatureSnapshot]:
    
    async with self.get_session() as session:
      stmt = (select(PlayerFeatureSnapshot)
        .where(PlayerFeatureSnapshot.gameweek >= start_gw)
        .where(PlayerFeatureSnapshot.gameweek <= end_gw)
        .where(PlayerFeatureSnapshot.team_name == team_name)
        .order_by(PlayerFeatureSnapshot.gameweek, PlayerFeatureSnapshot.player_id)
      )

      result = await session.execute(stmt)
      
      return list(result.scalars().all())
