import os
from typing import List

import httpx


class FPLService:
  def __init__(self):
    self.api_base_url = os.getenv('FPL_API_BASE_URL')

  async def fetch_all_players(self) -> List[dict]:

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

  async def get_player_detials(self, player_id: int) -> dict:
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


def get_fpl_service() -> FPLService:
    return FPLService()
    
