from typing import List, Optional

from sqlalchemy import desc, select

from backend.app.models.ml.team_feature_snapshot import TeamFeatureSnapshot
from backend.app.db.database_config import DatabaseConfig
from backend.app.repositories.base_repository import BaseRepository


class TeamFeatureRepository(BaseRepository):  
  def __init__(self, db_config: DatabaseConfig):
    super().__init__(db_config)

  async def bulk_insert(self, snapshots: List[TeamFeatureSnapshot]) -> int:

    if not snapshots:
      return 0
    
    async with self.get_session() as session:
      db_snapshots = [
        TeamFeatureSnapshot(**snap.nodel_dump())
        for snap in snapshots
      ]

      session.add_all(db_snapshots)
      return len(db_snapshots)
    
  async def get_by_gameweek(self, gameweek: int) -> List[TeamFeatureSnapshot]:
    async with self.get_session() as session:
      stmt = select(TeamFeatureSnapshot).where(
        TeamFeatureSnapshot.gameweek == gameweek
      )

      result = await session.execute(stmt)
      
      return list(result.scalars().all())
    
  async def get_by_gameweek_range(self, start_gw: int, end_gw: int) -> List[TeamFeatureSnapshot]:
    async with self.get_session() as session:
      stmt = (select(TeamFeatureSnapshot)
        .where(TeamFeatureSnapshot.gameweek >= start_gw)
        .where(TeamFeatureSnapshot <= end_gw)
      )
      
      result = await session.execute(stmt)
      
      return list(result.scalars().all())

  async def get_by_team_and_gameweek(self, team_name: str, gameweek: int) -> List[TeamFeatureSnapshot]:
    async with self.get_session() as session:
      stmt = (select(TeamFeatureSnapshot)
        .where(TeamFeatureSnapshot.team_name == team_name)
        .where(TeamFeatureSnapshot.gameweek == gameweek)
      )
      
      result = await session.execute(stmt)
      
      return list(result.scalars().all())
  
  async def get_latest_by_team(self, team_name: str, limit: int = 10):
    async with self.get_session() as session:
      stmt = (select(TeamFeatureSnapshot)
        .where(TeamFeatureSnapshot.team_name == team_name)
        .order_by(desc(TeamFeatureSnapshot.snapshot_time))
        .limit(limit)
      )
      
      result = await session.execute(stmt)
      
      return list(result.scalars().all())
    
  async def get_training_data(self, 
    start_gw: int, 
    end_gw: int, 
    team_name: Optional[str] = None
  ) -> List[TeamFeatureSnapshot]:
    
    async with self.get_session() as session:
      stmt = (select(TeamFeatureSnapshot)
        .where(TeamFeatureSnapshot.gameweek >= start_gw)
        .where(TeamFeatureSnapshot.gameweek <= end_gw)
        .where(TeamFeatureSnapshot.team_name == team_name)
        .order_by(TeamFeatureSnapshot.gameweek, TeamFeatureSnapshot.player_id)
      )

      result = await session.execute(stmt)
      
      return list(result.scalars().all())