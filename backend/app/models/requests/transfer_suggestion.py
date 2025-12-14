from typing import Optional
from pydantic import BaseModel


class TransferSuggestionRequest(BaseModel):
  budget: float
  position: Optional[str] = None
  num_recommendations: int = 3