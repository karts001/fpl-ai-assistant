from backend.app.models.dtos.player_season_history_dto import PlayerSeasonHistoryDTO
from backend.app.models.raw.raw_player_season_history import RawPlayerSeasonHistory


def map_raw_player_season_history_to_dto(raw: RawPlayerSeasonHistory) -> PlayerSeasonHistoryDTO:

  return PlayerSeasonHistoryDTO(
    season_name=raw.season,
    total_points=raw.total_points,
    minutes=raw.minutes,
    goals_scored=raw.goals_scored,
    assists=raw.assists,
    clean_sheets=raw.clean_sheets,
    goals_conceded=raw.goals_conceded,
    own_goals=raw.own_goals,
    penalties_saved=raw.penalties_saved,
    saves=raw.saves,
    penalties_missed=raw.penalties_missed,
    yellow_cards=raw.yellow_cards,
    red_cards=raw.red_cards,
    bonus=raw.bonus,
    bps=raw.bps,
    influence=raw.influence,
    creativity=raw.creativity,
    threat=raw.threat,
    ict_index=raw.ict_index,
    expected_goals=raw.expected_goals,
    expected_assists=raw.expected_assists,
    expected_goal_involvements=raw.expected_goal_involvements,
    expected_goals_conceded=raw.expected_goals_conceded
  )