import datetime
from sqlalchemy import String, DateTime, Integer, Float, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base


class PlayerFeatureSnapshot(Base):
  __tablename__ = 'player_feature_snapshots'
  
  id: Mapped[int] = mapped_column(primary_key=True)

  player_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
  team_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
  gameweek: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

  minutes_last_5: Mapped[int] = mapped_column(Integer, nullable=False)
  goals_last_5: Mapped[int] = mapped_column(Integer, nullable=False)
  assists_last_5: Mapped[int] = mapped_column(Integer, nullable=False)

  xg_last_5: Mapped[float] = mapped_column(Float, nullable=False)
  xa_last_5: Mapped[float] = mapped_column(Float, nullable=False)
  ict_last_5: Mapped[float] = mapped_column(Float, nullable=False)

  appearances_last_5: Mapped[int] = mapped_column(Integer, nullable=False)

  is_home: Mapped[bool] = mapped_column(Boolean, nullable=False)
  opponent_team: Mapped[str] = mapped_column(String(50), nullable=False)
  opponent_difficulty: Mapped[int] = mapped_column(Integer, nullable=False)

  snapshot_time: Mapped[datetime.datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    index=True
  )

