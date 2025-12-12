from backend.app.models.dtos.player_dto import PlayerDTO
from backend.app.models.raw.raw_player import RawPlayer


POSITION_MAP = {
  1: "Goalkeeper",
  2: "Defender",
  3: "Midfielder",
  4: "Forward"
}

TEAM_MAP = {
  1: "Arsenal",
  2: "Aston Villa",
  3: "Burnley",
  4: "Bournemouth",
  5: "Brentford",
  6: "Brighton",
  7: "Chelsea",
  8: "Crystal Palace",
  9: "Everton",
  10: "Fulham",
  11: "Leeds",
  12: "Liverpool",
  13: "Man City",
  14: "Man Utd",
  15: "Newcastle",
  16: "Nott'm Forest",
  17: "Sunderland",
  18: "Spurs",
  19: "West Ham",
  20: "Wolves"
}

def map_raw_player_to_dto(raw: RawPlayer, team_map: dict = None):
  
  if team_map is None:
    team_map = TEAM_MAP

  price = raw.now_cost / 10.0
  points = raw.total_points
  values_rating = points / price if price > 0 else 0.0

  if raw.form >= 6.0:
    form_rating = "Hot"
  elif raw.form >= 3.0:
    form_rating = "Warm"
  else:
    form_rating = "Cold"

  return PlayerDTO(
    id=raw.id,
    name=f"{raw.first_name} {raw.second_name}",
    team_name=team_map.get(raw.team, "Unknown"),
    position=POSITION_MAP.get(raw.element_type, "Unknown"),
    price=price,
    ownership=raw.selected_by_percent,
    form=raw.form,
    points=points,
    minutes=raw.minutes,
    goals=raw.goals_scored,
    assists=raw.assists,
    clean_sheets=raw.clean_sheets,
    expected_goals=raw.ep_this,
    expected_assists=raw.ep_next,
    value_rating=values_rating,
    form_rating=form_rating
  )

