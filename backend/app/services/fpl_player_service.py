import asyncio
import datetime
from typing import Dict, List, Tuple

from backend.app.core.fpl_api_client import FPLApiClient
from backend.app.models.dtos.player_analysis_dto import PlayerAnalysisDTO
from backend.app.models.dtos.player_dto import PlayerDTO
from backend.app.models.mappers.player_fixture_mapper import map_raw_player_fixture_to_dto
from backend.app.models.mappers.player_gameweek_mapper import map_raw_player_gameweek_stats_to_dto
from backend.app.models.mappers.player_mapper import map_raw_player_to_dto
from backend.app.models.mappers.player_season_history_mapper import map_raw_player_season_history_to_dto
from backend.app.models.raw.raw_player import RawPlayer
from backend.app.models.raw.raw_player_summary import RawPlayerSummary
from backend.app.utils.maps import TEAM_MAP_25_26


class FPLService:
  def __init__(self, api_client: FPLApiClient):
    self.api_client = api_client
    self._player_summary_cache: Dict[int, Tuple[dict, datetime.time]] = {}
    self._cache_ttl_minutes = 120  # 2 hours

  async def _get_player_summary(self, player_id: int, force_refresh: bool = False) -> RawPlayerSummary:

    now = datetime.datetime.now()

    if force_refresh and player_id in self._player_summary_cache:
      cached_data, cached_time = self._player_summary_cache[player_id]
      
      if now - cached_time < datetime.timedelta(minutes=self._cache_ttl_minutes):
        return cached_data
        
    response = await self.api_client._get(f'/element-summary/{player_id}/')
    self._player_summary_cache[player_id] = (response, now)
    
    return response

  async def get_player_for_analysis(self, player_id: int) -> PlayerAnalysisDTO:
    response = await self.api_client._get(f'/element-summary/{player_id}/')

    return PlayerAnalysisDTO(
      player_id=player_id,
      upcoming_fixtures=[map_raw_player_fixture_to_dto(f, TEAM_MAP_25_26) for f in response.get('fixtures', [])],
      recent_gameweeks=[map_raw_player_gameweek_stats_to_dto(gw, TEAM_MAP_25_26) for gw in response.get('history', [])],
      season_history=[map_raw_player_season_history_to_dto(sh) for sh in response.get('history_past', [])]
    )

  async def get_multiple_players_for_analysis(self, player_ids: List[int]) -> List[PlayerAnalysisDTO]:
    return await asyncio.gather(*[
      self.get_player_for_analysis(pid) for pid in player_ids
    ])
  
  async def get_all_players(self) -> List[PlayerDTO]:
     response = await self.api_client._get('/bootstrap-static/')

     return [map_raw_player_to_dto(RawPlayer(**p), TEAM_MAP_25_26) for p in response.get('elements', [])]


def get_fpl_service() -> FPLService:
    api_client = FPLApiClient()
    return FPLService(api_client)
    
