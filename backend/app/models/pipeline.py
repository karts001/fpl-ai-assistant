import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ProcessingStatus(Enum):
  SUCCESS = 'success'
  FAILED = 'fail'
  SKIPPED = 'already_processed'

class DataPipelineResult(BaseModel):
  as_of_gw: int
  players_stored: int
  teams_stored: int
  timestamp: datetime.datetime

class PipelineSummary(BaseModel):
  status: ProcessingStatus
  start_time: datetime.datetime
  reason: Optional[str] = None
  duration: Optional[int] = 0
  gameweek: int
  players_stored: Optional[int] = 0
  teams_stored: Optional[int] = 0
  error: Optional[str]
