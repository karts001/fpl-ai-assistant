from datetime import datetime
from typing import List, Tuple
from backend.app.models.data_pipeline_summary import DataPipelineSUmmary, DataPipelineResult
from backend.app.models.ml.player_feature_snapshot import PlayerFeatureSnapshot
from backend.app.models.ml.team_feature_snapshot import TeamFeatureSnapshot
from backend.app.repositories.player_feature_repository import PlayerFeatureRepository
from backend.app.repositories.team_feature_repository import TeamFeatureRepository
from backend.app.services.feature_builder_service import FeatureBuilderService
from backend.app.services.fpl_service import FPLService


class DataPipeline:
  def __init__(self, 
    fpl_service: FPLService, 
    feature_builder: FeatureBuilderService,
    player_repo: PlayerFeatureRepository,
    team_repo: TeamFeatureRepository
  ):
    self.fpl_service = fpl_service
    self.feature_builder = feature_builder
    self.player_repo = player_repo
    self.team_repo = team_repo
  
  async def build_and_store_features_for_gameweek(
    self, 
    as_of_gw: int
  ) -> DataPipelineResult:
    
    # Step 1 fetch all players
    all_players = self.fpl_service.get_all_players()
    player_ids = [p.id for p in all_players]

    # Step 2 build PlayerAnalysisDTOs
    player_analysis = self.fpl_service.get_multiple_players_for_analysis(player_ids)

    # Step 3 build player level snapshots
    player_snapshots = []
    for analysis in player_analysis:
      player_snapshots.extend(self.feature_builder.build_player_features(analysis, as_of_gw))

    # Step 4 build team level snapshots
    team_snapshots = self.feature_builder.build_team_features(player_snapshots, as_of_gw)

    # Step 5 store features in database
    player_count = await self.player_repo.bulk_insert(player_snapshots)
    team_count = await self.team_repo.bulk_insert(team_snapshots)

    return DataPipelineResult(
      as_of_gw,
      players_stored=player_count,
      teams_stored=team_count,
      timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
