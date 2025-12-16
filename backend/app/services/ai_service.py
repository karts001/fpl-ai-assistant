import os
from typing import List, Optional

from dotenv import load_dotenv
from google import genai

from backend.app.factories.llm_factory import get_llm
from backend.app.llm.base_llm import BaseLLM
from backend.app.models.dtos.player_analysis_dto import PlayerAnalysisDTO
from backend.app.models.dtos.player_dto import PlayerDTO

load_dotenv()


class AIService:
  def __init__(self, llm: BaseLLM):
    
    self.llm = llm

  def format_player_for_prompt(self, player: PlayerDTO) ->str:
    return f"""
    Player Name: {player.name}
    Team: {player.team_name}
    Position: {player.position}
    Price: {player.price} million
    Ownership: {player.ownership}%
    Form: {player.form}
    Total Points: {player.points}
    Minutes Played: {player.minutes}
    Goals: {player.goals}
    Assists: {player.assists}
    Clean Sheets: {player.clean_sheets}
    Expected Goals (xG): {player.expected_goals}
    Expected Assists (xA): {player.expected_assists}
    Value Rating: {player.value_rating}
    Form Rating: {player.form_rating}
    """
  
  def format_detailed_plyer_info_for_prompt(self, player: PlayerDTO, analysis: PlayerAnalysisDTO) -> str:

    fixtures_text = '\nUpcoming Fixtures:\n'

    for fixtures in analysis.upcoming_fixtures:
      home_away = 'vs' if fixtures.is_home else '@'
      fixtures_text += f" GW{fixtures.gameweek}: {home_away} {fixtures.opponent_team} (Difficulty: {fixtures.difficulty})\n"

    recent_form_text = '\nRecent Gameweeks:\n'

    for gw in analysis.recent_gameweeks:
      recent_form_text += f" GW{gw.gameweek}: Points: {gw.points}, xG: {gw.expected_goals}, xA: {gw.expected_assists}, Minutes: {gw.minutes}\n"
    
    season_history_text = '\nSeason History:\n'

    for sh in analysis.season_history:
      season_history_text += f" GW{sh.gameweek}: Points: {sh.total_points}, xG: {sh.expected_goals}, xA: {sh.expected_assists}, Minutes: {sh.minutes}\n"

    
    return f"""
      General Info:
      - Player Name: {player.name}
      - Team: {player.team_name}
      - Position: {player.position}
      - Price: {player.price} million
      - Ownership: {player.ownership}%

      Current Season Stats:
      - Total Points: {player.points}
      - Form: {player.form}
      - Goals: {player.goals}
      - Assists: {player.assists}
      - Clean Sheets: {player.clean_sheets}
      - Expected Goals (xG): {player.expected_goals}
      - Expected Assists (xA): {player.expected_assists}
      - Value Rating: {player.value_rating}
      - Form Rating: {player.form_rating}
      - Minutes Player: {player.minutes}

      {fixtures_text}
      {recent_form_text}
      {season_history_text}
    """
  
  async def suggest_transfers(
    self,
    budget: float,
    position: Optional[str] = None,
    players: Optional[List[PlayerDTO]] = None,
    num_recommendations: int = 3
  ) -> dict:
    
    if not players:
      raise ValueError("Player list cannot be empty for transfer suggestions")

    # Filter candidates which fit in budget
    candidates = [p for p in players if p.price <= budget]

    # Further filter by position if specified
    if position:
      candidates = [p for p in candidates if p.position.lower() == position.lower()]

    # Sort candidates by form descending and take top 20
    candidates = sorted(candidates, key=lambda x: x.form or 0, reverse=True)[:20]

    player_text = "\n---\n".join([self.format_player_for_prompt(p) for p in candidates])

    if not candidates:
      return {
        "recomendations": [],
        "message": f"No players found under £{budget}m" + (f"for position {position}" if position else "")
      }

    # Build prompt
    prompt = f"""
      You are a Fantasy Premier League (FPL) expert. Suggest {num_recommendations}
      transfer options within a budget of {budget} million.
      {"Focus on the position: " + position if position else ""}

      Here are the candidate players: {player_text}

      Provide your top {num_recommendations} recommendations. For each player, explain:
      1. Why they're a good pick right now
      2. Their recent form and underlying stats
      3. Value for money
      4. Any concerns or risks

      Format your response as a clear, numbered list with each recommendation followed by your analysis.
    """

    try:
      response = await self.llm.generate_content_async(prompt)

      return {
        "recommendations": response.text,
        "criteria": {
          "budget": budget,
          "position": position,
          "candidates analysed": len(candidates)
        }
      }
    except Exception as e:
      raise Exception(f"AI service error: {str(e)}")

  async def analyse_player_detailed(
    self,
    player: PlayerDTO,
    analysis: PlayerAnalysisDTO
  ) -> dict:
    """Deep analysis of a single player

    Args:
        player (PlayerDTO): Basic and general player info
        analysis (PlayerAnalysisDTO): Detialed player stats and metrics

    Returns:
        dict: AI analysis result
    """

    player_info = self.format_player_for_prompt(player)
    analysis_info = f"""
    Detailed Stats:
    - Expected Goals (xG): {analysis.expected_goals}
    - Expected Assists (xA): {analysis.expected_assists}
    - Expected Goal Involvements (xGI): {analysis.expected_goal_involvements}
    - Expected Goals Conceded (xGC): {analysis.expected_goals_conceded}
    - Shots on Target per 90: {analysis.shots_on_target_per_90}
    - Key Passes per 90: {analysis.key_passes_per_90}
    - Tackles per 90: {analysis.tackles_per_90}
    - Interceptions per 90: {analysis.interceptions_per_90}
    - Clearances per 90: {analysis.clearances_per_90}
    - Aerial Duels Won per 90: {analysis.aerial_duels_won_per_90}
    - Form Trend: {analysis.form_trend}
    - Injury History: {analysis.injury_history}
    - Upcoming Fixtures Difficulty: {analysis.upcoming_fixtures_difficulty}
    """

    prompt = f"""
      You are a Fantasy Premier League (FPL) expert. Provide a deep analysis of the following player:

      {player_info}

      {analysis_info}

      Analyze the player's recent performance, underlying stats, and future potential.
      Highlight strengths, weaknesses, and any risks associated with selecting this player.
      Provide actionable insights for FPL managers considering this player for their team.
    """

    try:
      response = self.llm.generate_content_async(prompt)

      return {
        "player": player.name,
        "player_analysis": response.text
      }
    except Exception as e:
      raise Exception(f"AI service error: {str(e)}")

def get_ai_service() -> AIService:
    llm = get_llm()
    return AIService(llm)