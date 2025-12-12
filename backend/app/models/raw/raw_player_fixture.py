from pydantic import BaseModel


class RawPlayerFixture(BaseModel):
  id: int
  code: int
  team_h: int
  team_h_score: int | None
  team_a: int
  team_a_score: int | None
  event: int
  finished: bool
  minutes: int
  provisional_start_time: str
  kickoff_time: str
  event_name: str
  is_home: bool
  difficulty: int
  