from backend.app.models.dtos.player_fixture_dto import PlayerFixtureDTO
from backend.app.models.raw.raw_player_fixture import RawPlayerFixture


def map_raw_player_fixture_to_dto(raw: RawPlayerFixture, team_map: dict) -> PlayerFixtureDTO:

  return PlayerFixtureDTO(
    gameweek=raw.event,
    opponent=team_map.get(raw.team_a if raw.is_home else raw.team_h, "Unknown"),
    is_home=raw.is_home,
    difficulty=raw.difficulty,
    kick_off_time=raw.kickoff_time
  )