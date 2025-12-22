from typing import List
from pydantic import BaseModel

from backend.app.models.dtos.player_fixture_dto import PlayerFixtureDTO
from backend.app.models.dtos.player_gameweek_stats_dto import PlayerGameweekStatsDTO
from backend.app.models.dtos.player_season_history_dto import PlayerSeasonHistoryDTO


class PlayerAnalysisDTO(BaseModel):
  player_id: int
  team_name: str
  upcoming_fixtures: List[PlayerFixtureDTO]
  recent_gameweeks: List[PlayerGameweekStatsDTO]
  season_history: List[PlayerSeasonHistoryDTO]