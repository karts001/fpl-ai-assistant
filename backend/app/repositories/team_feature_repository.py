from typing import List, Optional

from sqlalchemy import desc, select

from backend.app.db.models.team_feature_snapshot_sql import TeamFeatureSnapshotSQL
from backend.app.db.database_config import DatabaseConfig
from backend.app.repositories.base_repository import BaseRepository


class TeamFeatureRepository(BaseRepository):  
  def __init__(self, db_config: DatabaseConfig):
    super().__init__(db_config)

  async def bulk_insert(self, snapshots: List[TeamFeatureSnapshotSQL]) -> int:

    if not snapshots:
      return 0
    
    async with self.get_session() as session:
      db_snapshots = [
        TeamFeatureSnapshotSQL(**snap.nodel_dump())
        for snap in snapshots
      ]

      session.add_all(db_snapshots)
      return len(db_snapshots)
    
  async def get_by_gameweek(self, gameweek: int) -> List[TeamFeatureSnapshotSQL]:
    async with self.get_session() as session:
      stmt = select(TeamFeatureSnapshotSQL).where(
        TeamFeatureSnapshotSQL.gameweek == gameweek
      )

      result = await session.execute(stmt)
      
      return result.scalars().all()
    
  async def get_by_gameweek_range(self, start_gw: int, end_gw: int) -> List[TeamFeatureSnapshotSQL]:
    async with self.get_session() as session:
      stmt = (select(TeamFeatureSnapshotSQL)
        .where(TeamFeatureSnapshotSQL.gameweek >= start_gw)
        .where(TeamFeatureSnapshotSQL.gameweek <= end_gw)
      )
      
      result = await session.execute(stmt)
      
      return list(result.scalars().all())

  async def get_by_team_and_gameweek(self, team_name: str, gameweek: int) -> List[TeamFeatureSnapshotSQL]:
    async with self.get_session() as session:
      stmt = (select(TeamFeatureSnapshotSQL)
        .where(TeamFeatureSnapshotSQL.team_name == team_name)
        .where(TeamFeatureSnapshotSQL.gameweek == gameweek)
      )
      
      result = await session.execute(stmt)
      
      return result.scalars().all()
  
  async def get_latest_by_team(self, team_name: str, limit: int = 10):
    async with self.get_session() as session:
      stmt = (select(TeamFeatureSnapshotSQL)
        .where(TeamFeatureSnapshotSQL.team_name == team_name)
        .order_by(desc(TeamFeatureSnapshotSQL.snapshot_time))
        .limit(limit)
      )
      
      result = await session.execute(stmt)
      
      return result.scalars().all()
    
  async def get_training_data(self, 
    start_gw: int, 
    end_gw: int, 
    team_name: Optional[str] = None
  ) -> List[TeamFeatureSnapshotSQL]:
    
    async with self.get_session() as session:
      stmt = (select(TeamFeatureSnapshotSQL)
        .where(TeamFeatureSnapshotSQL.gameweek >= start_gw)
        .where(TeamFeatureSnapshotSQL.gameweek <= end_gw)
        .where(TeamFeatureSnapshotSQL.team_name == team_name)
        .order_by(TeamFeatureSnapshotSQL.gameweek, TeamFeatureSnapshotSQL.player_id)
      )

      result = await session.execute(stmt)
      
      return result.scalars().all()