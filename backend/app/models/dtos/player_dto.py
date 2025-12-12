from typing import Optional
from pydantic import BaseModel


class PlayerDTO(BaseModel):
  """ Simplified Player model for frontend """
  id: int
  name: str
  team_name: str
  position: str  # "Goalkeeper", "Defender", "Midfielder", "Forward"
  price: float  # Converted to actual pounds (5.5)
  ownership: float  # Converted to percentage (12.5)
  form: float
  points: int
  minutes: int
  goals: int
  assists: int
  clean_sheets: int
  expected_goals: float
  expected_assists: float
  
  # Computed fields
  value_rating: Optional[float] = None  # Points per million
  form_rating: Optional[str] = None  # "Hot", "Warm", "Cold"
