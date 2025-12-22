import datetime
from pydantic import BaseModel


class PlayerGameweekStatsDTO(BaseModel):
  # General stats
  gameweek: int
  total_points: int
  minutes: int

  # Attacking stats
  goals_scored: int
  assists: int

  # Defensive stats 
  clean_sheets: int
  goals_conceded: int
  own_goals: int

  # Goalkeeping stats
  penalties_saved: int
  saves: int

  # Negative stats
  penalties_missed: int
  yellow_cards: int
  red_cards: int

  # Bonus system
  bonus: int
  bps: int

  # Value and ownership
  value: int
  transfers_in: int
  transfers_out: int
  selected: int

  # ICT stats
  influence: float
  creativity: float
  threat: float
  ict_index: float

  # Expected stats
  expected_goals: float
  expected_assists: float
  expected_goal_involvements: float
  expected_goals_conceded: float

  # Match details
  kickoff_time: datetime.datetime
  was_home: bool
  opponent_team: str