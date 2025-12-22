import datetime

from pydantic import BaseModel


class TeamFeatureSnapshot(BaseModel):
  # Identity
  team_name: str
  gameweek: int

  # Rolling form
  minutes_last_5: int
  goals_last_5: int
  assists_last_5: int
  xg_last_5: float
  xa_last_5: float
  ict_last_5: float
  appearances_last_5: int

  # Fixture context
  is_home: bool
  opponent_team: str
  opponent_difficulty: int

  # Metadata
  snapshot_time: datetime.datetime