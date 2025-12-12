from typing import List
from backend.app.models.dtos.player_gameweek_stats_dto import PlayerGameweekStatsDTO
from backend.app.models.raw.raw_player_gameweek_history import RawPlayerGameweekHistory


def map_raw_player_gameweek_stats_to_dto(raw: RawPlayerGameweekHistory, team_map: dict) -> PlayerGameweekStatsDTO:

  if team_map is None:
    team_map = TEAM_MAP_25_26
  
  return PlayerGameweekStatsDTO(
    gameweek=raw.round,
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
    value=raw.value,
    transfers_in=raw.transfers_in,
    transfers_out=raw.transfers_out,
    selected=raw.selected,
    influence=raw.influence,
    creativity=raw.creativity,
    threat=raw.threat,
    ict_index=raw.ict_index,
    expected_goals=raw.expected_go,
    expected_assists=raw.expected_assists,
    expected_goal_involvements=raw.expected_goal_involvements,
    expected_goals_conceded=raw.expected_goals_conceded,
    kickoff_time=raw.kickoff_time,
    was_home=raw.was_home,
    opponent_team=team_map.get(raw.opponent_team, "Unknown")
  )