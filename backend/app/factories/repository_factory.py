from backend.app.db.database_config import DatabaseConfig
from backend.app.repositories.player_feature_repository import PlayerFeatureRepository
from backend.app.repositories.team_feature_repository import TeamFeatureRepository


class RepositoryFactory:
  def __init__(self, db_config: DatabaseConfig):
    self.db_config = db_config

  def create_player_feature_repository(self) -> PlayerFeatureRepository:
    return PlayerFeatureRepository(self.config_db)
  
  def create_team_feature_repository(self) -> TeamFeatureRepository:
    return TeamFeatureRepository(self.config_db)