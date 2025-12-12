from backend.app.models.dtos.player_dto import PlayerDTO
from backend.app.models.raw.raw_player import RawPlayer
from backend.app.utils.maps import POSITION_MAP, TEAM_MAP_25_26


def map_raw_player_to_dto(raw: RawPlayer, team_map: dict) -> PlayerDTO:
  
  if team_map is None:
    team_map = TEAM_MAP_25_26

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

