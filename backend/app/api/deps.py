"""
Dependency injection for FastAPI routes and standalone scripts

FastAPI routes use the get_* functions with Depends()
Standalone scripts use the create_* functions directly
"""

from functools import lru_cache

from fastapi import Depends

from backend.app.core.config import Settings
from backend.app.core.fpl_api_client import FPLApiClient
from backend.app.db.database_config import DatabaseConfig
from backend.app.factories.llm_factory import get_llm
from backend.app.repositories.player_feature_repository import PlayerFeatureRepository
from backend.app.repositories.team_feature_repository import TeamFeatureRepository
from backend.app.services.ai_service import AIService
from backend.app.jobs.data_pipeline import DataPipeline
from backend.app.services.feature_builder_service import FeatureBuilderService
from backend.app.services.fpl_service import FPLService


# ============================================================================
# Core Dependencies (for FastAPI with Depends)
# ============================================================================

@lru_cache()
def get_settings() -> Settings:
  """Get application settings (cached singleton)"""
  return Settings()

def get_db_config(settings: Settings = Depends(get_settings)) -> DatabaseConfig:
  """Get database configuration (cached singleton)"""
  return DatabaseConfig(settings.database_url_async)


# ============================================================================
# Repository Dependencies (for FastAPI with Depends)
# ============================================================================

def get_player_repository(
    db_config: DatabaseConfig = Depends(get_db_config)
) -> PlayerFeatureRepository:
  """Get player feature repository"""
  return PlayerFeatureRepository(db_config)


def get_team_repository(
    db_config: DatabaseConfig = Depends(get_db_config)
) -> TeamFeatureRepository:
  """Get team feature repository"""
  return TeamFeatureRepository(db_config)


# ============================================================================
# Service Dependencies (for FastAPI with Depends)
# ============================================================================

def get_api_client() -> FPLApiClient:
  """Get FPL API client"""
  return FPLApiClient()


def get_fpl_service(
    api_client: FPLApiClient = Depends(get_api_client)
) -> FPLService:
  """Get FPL service"""
  return FPLService(api_client)


def get_feature_builder_service() -> FeatureBuilderService:
  """Get feature builder service"""
  return FeatureBuilderService(rolling_window=5)


def get_data_pipeline_service(
    fpl_service: FPLService = Depends(get_fpl_service),
    feature_builder: FeatureBuilderService = Depends(get_feature_builder_service),
    player_repo: PlayerFeatureRepository = Depends(get_player_repository),
    team_repo: TeamFeatureRepository = Depends(get_team_repository)
) -> DataPipeline:
  """Get data pipeline service (for FastAPI routes)"""
  return DataPipeline(
    fpl_service,
    feature_builder,
    player_repo,
    team_repo
  )


def get_ai_service() -> AIService:
  """Get AI service"""
  llm = get_llm()
  return AIService(llm)


# ============================================================================
# Factory Functions (for standalone scripts without Depends)
# ============================================================================

def create_player_repository() -> PlayerFeatureRepository:
  """
  Create player repository without FastAPI Depends
  Use this in standalone scripts, tests, or background jobs
  """
  settings = get_settings()
  db_config = get_db_config(settings)
  return PlayerFeatureRepository(db_config)


def create_team_repository() -> TeamFeatureRepository:
  """
  Create team repository without FastAPI Depends
  Use this in standalone scripts, tests, or background jobs
  """
  settings = get_settings()
  db_config = get_db_config(settings)
  return TeamFeatureRepository(db_config)


def create_fpl_service() -> FPLService:
  """
  Create FPL service without FastAPI Depends
  Use this in standalone scripts, tests, or background jobs
  """
  api_client = get_api_client()
  return FPLService(api_client)


def create_data_pipeline_service() -> DataPipeline:
  """
  Create complete data pipeline service without FastAPI Depends
  Use this in standalone scripts, tests, or background jobs
  
  Example:
    pipeline = create_data_pipeline_service()
    result = await pipeline.build_and_store_features_for_gameweek(18)
  """
  settings = get_settings()
  db_config = get_db_config(settings)
  
  api_client = get_api_client()
  fpl_service = FPLService(api_client)
  feature_builder = get_feature_builder_service()
  player_repo = PlayerFeatureRepository(db_config)
  team_repo = TeamFeatureRepository(db_config)
  
  return DataPipeline(
    fpl_service,
    feature_builder,
    player_repo,
    team_repo
  )


def create_ai_service() -> AIService:
  """
  Create AI service without FastAPI Depends
  Use this in standalone scripts, tests, or background jobs
  """
  llm = get_llm()
  return AIService(llm)