from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  app_name: str = 'FPL AI Assistant'
  debug: bool = True
  api_version: str = 'v1'
  database_url: str

  class Config:
    env_file = '.env'
    env__file_encoding = 'utf-8'
   