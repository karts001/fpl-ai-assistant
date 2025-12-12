import os
from typing import List

import httpx

from backend.app.models.dtos.player_dto import PlayerDTO
from backend.app.models.dtos.player_fixture_dto import PlayerFixtureDTO
from backend.app.models.mappers.player_fixture_mapper import map_raw_player_fixture_to_dto
from backend.app.models.mappers.player_mapper import map_raw_player_to_dto
from backend.app.models.raw.raw_player import RawPlayer


class FPLService:
  def __init__(self):
    self.api_base_url = os.getenv('FPL_API_BASE_URL')

  async def fetch_all_players_raw(self) -> List[RawPlayer]:
    """ Fetch list of all players from FPL api

    Raises:
        ValueError: _description_

    Returns:
        List[RawPlayer]: List of RawPlayer objects
    """
    if not self.api_base_url:
        raise ValueError('FPL_API_BASE_URL environment variable is not set')
    
    try:
      async with httpx.AsyncClient() as client:
        response = await client.get(f'{self.api_base_url}/bootstrap-static/')
        response.raise_for_status()
        data = response.json()
        elements = data.get('elements', [])

        return elements
    except httpx.HTTPError as e:
      print(f'Error fetching players: {e}')
      raise

  async def get_all_players(self) -> List[PlayerDTO]:
    """Map raw player object to DTO

    Returns:
        List[PlayerDTO]: List of PlayerDTO objects
    """

    raw_players = await self.fetch_all_players_raw()
    player_dtos = [map_raw_player_to_dto(p) for p in raw_players]

    return player_dtos

  async def get_player_detials(self, player_id: int) -> dict:
    """Retreive details about an individual player

    Args:
        player_id (int): Player id as defined in FPL API

    Raises:
        ValueError: _description_

    Returns:
        dict: _description_
    """
    if not self.api_base_url:
        raise ValueError('FPL_API_BASE_URL environment variable is not set')
    
    try:
      async with httpx.AsyncClient() as client:
        response = await client.get(f'{self.api_base_url}/element-summary/{player_id}/')
        response.raise_for_status()
        data = response.json()

        return data
    except httpx.HTTPError as e:
      print(f'Error fetching player details for player ID {player_id}: {e}')
      raise

  async def fetch_player_fixtures(self, player_id: int) -> List[PlayerFixtureDTO]:
    if not self.api_base_url:
        raise ValueError('FPL_API_BASE_URL environment variable is not set')
    
    try:
      async with httpx.AsyncClient() as client:
        response = await client.get(f'{self.api_base_url}/element-summary/{player_id}/fixtures')
        response.raise_for_status()
        data = response.json()

        raw_fixtures = data.get('fixtures', [])
        fixtures = map_raw_player_fixture_to_dto(raw_fixtures)

        return fixtures
    except httpx.HTTPError as e:
      print(f'Error fetching player fixtures for player ID {player_id}: {e}')
      raise


def get_fpl_service() -> FPLService:
    return FPLService()
    
