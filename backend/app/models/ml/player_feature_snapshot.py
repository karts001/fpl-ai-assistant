import datetime
from pydantic import BaseModel


class PlayerFeatureSnapshot(BaseModel):
  player_id: int
  team_name: str
  gameweek: int

  # Rolling stats for last N gameweeks
  minutes_last_5: int
  goals_last_5: int
  assists_last_5: int
  xg_last_5: float
  xa_last_5: float
  ict_last_5: float
  appearances_last_5: int

  # Fixture info
  is_home: bool
  opponent_team: str
  opponent_difficulty: int

  snapshot_time: datetime.datetime