import datetime
from pydantic import BaseModel


class PlayerFixtureDTO(BaseModel):
  gameweek: int
  opponent: str
  is_home: bool
  difficulty: int # 1- 5 scale
  kick_off_time: datetime.datetime
