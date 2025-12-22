from collections import defaultdict
import datetime
from typing import List

from backend.app.models.ml.team_feature_snapshot import TeamFeatureSnapshot
from backend.app.models.dtos.player_analysis_dto import PlayerAnalysisDTO
from backend.app.models.ml.player_feature_snapshot import PlayerFeatureSnapshot
from backend.app.models.dtos.player_gameweek_stats_dto import PlayerGameweekStatsDTO


class FeatureBuilderService:
  def __init__(
    self, 
    rolling_window: int = 5,
    clock=lambda: datetime.datetime.now(datetime.timezone.utc)
  ):
    self.rolling_window = rolling_window
    self.clock = clock

  def _last_n_gameweek(self, gameweeks: List[PlayerGameweekStatsDTO], as_of_gw: int) -> List[PlayerGameweekStatsDTO]:
    filtered = [gw for gw in gameweeks if gw.gameweek < as_of_gw]
    return sorted(filtered, key=lambda x: x.gameweek)[-self.rolling_window:]
  
  def build_player_features(self, analysis: PlayerAnalysisDTO, as_of_gw: int) -> List[PlayerFeatureSnapshot]:
    snapshots = []

    last_n_gws = self._last_n_gameweek(analysis.recent_gameweeks, as_of_gw)

    # If no history yet, skip
    if not last_n_gws:
      return snapshots

    # Sum/aggregate rolling stats
    minutes = sum(gw.minutes for gw in last_n_gws)
    goals = sum(gw.goals_scored for gw in last_n_gws)
    assists = sum(gw.assists for gw in last_n_gws)
    xg = sum(gw.expected_goals for gw in last_n_gws)
    xa = sum(gw.expected_assists for gw in last_n_gws)
    ict = sum(gw.ict_index for gw in last_n_gws)
    appearances = len(last_n_gws)

    # Loop over upcoming fixtures for the GW
    for fixture in analysis.upcoming_fixtures:
      if fixture.gameweek != as_of_gw:
        continue
      
      snapshot = PlayerFeatureSnapshot(
        player_id=analysis.player_id,
        team_name=analysis.team_name,
        gameweek=fixture.gameweek,
        minutes_last_5=minutes,
        goals_last_5=goals,
        assists_last_5=assists,
        xg_last_5=xg,
        xa_last_5=xa,
        ict_last_5=ict,
        appearances_last_5=appearances,
        is_home=fixture.is_home,
        opponent_team=fixture.opponent,
        opponent_difficulty=fixture.difficulty,
        snapshot_time=self.clock()
      )

      snapshots.append(snapshot)

    return snapshots
  
  def build_team_features(self,
    player_snapshots: List[PlayerFeatureSnapshot], 
    as_of_gw: int
  )-> List[TeamFeatureSnapshot]:
    
    team_agg = defaultdict(lambda: {
      "minutes_last_5": 0,
      "goals_last_5": 0,
      "assists_last_5": 0,
      "xg_last_5": 0.0,
      "xa_last_5": 0.0,
      "ict_last_5": 0.0,
      "appearances_last_5": 0,
      "fixture": None  # store first fixture found for optional info
    })

    for snap in player_snapshots:
      if snap.gameweek != as_of_gw:
          continue
      team = snap.team_name
      team_agg[team]["minutes_last_5"] += snap.minutes_last_5
      team_agg[team]["goals_last_5"] += snap.goals_last_5
      team_agg[team]["assists_last_5"] += snap.assists_last_5
      team_agg[team]["xg_last_5"] += snap.xg_last_5
      team_agg[team]["xa_last_5"] += snap.xa_last_5
      team_agg[team]["ict_last_5"] += snap.ict_last_5
      team_agg[team]["appearances_last_5"] += snap.appearances_last_5

      # Keep a reference to the fixture (home/away, opponent, difficulty)
      if not team_agg[team]["fixture"]:
          team_agg[team]["fixture"] = snap

    # Convert aggregated dict into TeamFeatureSnapshotDTOs
    team_features = []
    for team_name, agg in team_agg.items():
      fixture_snap = agg["fixture"]
      team_features.append(
        TeamFeatureSnapshot(
          team_name=team_name,
          gameweek=as_of_gw,
          minutes_last_5=agg["minutes_last_5"],
          goals_last_5=agg["goals_last_5"],
          assists_last_5=agg["assists_last_5"],
          xg_last_5=agg["xg_last_5"],
          xa_last_5=agg["xa_last_5"],
          ict_last_5=agg["ict_last_5"],
          appearances_last_5=agg["appearances_last_5"],
          is_home=fixture_snap.is_home if fixture_snap else False,
          opponent_team=fixture_snap.opponent_team if fixture_snap else "",
          opponent_difficulty=fixture_snap.opponent_difficulty if fixture_snap else 0,
          snapshot_time=self.clock()
        )
      )

    return team_features