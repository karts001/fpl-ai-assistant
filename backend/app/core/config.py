from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  app_name: str = 'FPL AI Assistant'
  debug: bool = True
  api_version: str = 'v1'
  database_url: str
  database_url_async: str

  # FPL API
  fpl_api_base_url: str = 'https://fantasy.premierleague.com/api/'  # ← ADD THIS
  
  # LLM Configuration
  llm_provider: str = 'gemini'  # ← ADD THIS
  gemini_api_key: str  # ← ADD THIS
  gemini_model: str = 'gemini-2.5-flash'  # ← ADD THIS

  class Config:
    env_file = '.env'
    env__file_encoding = 'utf-8'
   