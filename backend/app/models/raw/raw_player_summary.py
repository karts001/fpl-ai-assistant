from typing import List

from pydantic import BaseModel
from backend.app.models.raw.raw_player_fixture import RawPlayerFixture
from backend.app.models.raw.raw_player_gameweek_history import RawPlayerGameweekHistory
from backend.app.models.raw.raw_player_season_history import RawPlayerSeasonHistory


class RawPlayerSummary(BaseModel):
  fixtures: List[RawPlayerFixture]
  history: List[RawPlayerGameweekHistory]
  history_past: List[RawPlayerSeasonHistory]