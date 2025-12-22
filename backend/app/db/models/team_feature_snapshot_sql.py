import datetime

from sqlalchemy import Boolean, String, DateTime, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeamFeatureSnapshotSQL(Base):
  __tablename__ = 'team_feature_snapshots'

  id: Mapped[int] = mapped_column(primary_key=True)

  # Identity
  team_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
  gameweek: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

  # Aggregated rolling stats
  minutes_last_5: Mapped[int] = mapped_column(Integer, nullable=False)
  goals_last_5: Mapped[int] = mapped_column(Integer, nullable=False)
  assists_last_5: Mapped[int] = mapped_column(Integer, nullable=False)

  xg_last_5: Mapped[float] = mapped_column(Float, nullable=False)
  xa_last_5: Mapped[float] = mapped_column(Float, nullable=False)
  ict_last_5: Mapped[float] = mapped_column(Float, nullable=False)

  appearances_last_5: Mapped[int] = mapped_column(Integer, nullable=False)

  # Fixture context
  is_home: Mapped[bool] = mapped_column(Boolean, nullable=False)
  opponent_team: Mapped[str] = mapped_column(String(50), nullable=False)
  opponent_difficulty: Mapped[int] = mapped_column(Integer, nullable=False)

  # Metadata
  snapshot_time: Mapped[datetime.datetime] = mapped_column(
    DateTime(timezone=True),
    index=True
  )