import os
from typing import List, Optional

from dotenv import load_dotenv
from google import genai

from backend.app.models.dtos.player_analysis_dto import PlayerAnalysisDTO
from backend.app.models.dtos.player_dto import PlayerDTO

load_dotenv()


class AIService:
  def __init__(self):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
      raise ValueError("GEMINI_API_KEY environment variable not set")
    
    self.client = genai.Client()
    self.model= "gemini-2.5-flash"

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
      response = self.client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
      )

      return {
        "recommendations": response.text,
        "criteria": {
          "budget": budget,
          "position": position,
          "candidates analysed": len(candidates)
        }
      }
    except Exception as e:
      raise Exception(f"Ai service error: {str(e)}")

  async def analyse_player_detailed(
    self,
    player: PlayerDTO,
    analysis: PlayerAnalysisDTO
  ) -> str:
    pass

def get_ai_service() -> AIService:
    return AIService()