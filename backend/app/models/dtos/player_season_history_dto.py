from pydantic import BaseModel


class PlayerSeasonHistoryDTO(BaseModel):
  season_name: str

  # Performance Metrics
  total_points: int
  minutes: int
  goals_scored: int
  assists: int
  clean_sheets: int
  goals_conceded: int
  own_goals: int
  penalties_saved: int
  penalties_missed: int
  yellow_cards: int
  red_cards: int
  saves: int
  bonus: int
  bps: int # bonus points scored

  # Match stats
  starts: int

  # Value Metrics
  start_cost: int
  end_cost: int

  # ICT Metrics
  influence: float
  creativity: float
  threat: float
  ict_index: float

  # Expected Metrics
  expected_goals: float
  expected_assists: float
  expected_goal_involvements: float
  expected_goals_conceded: float
  