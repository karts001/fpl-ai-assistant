import os
from typing import Optional

import httpx


class FPLApiClient:
  def __init__(self, base_url: Optional[str] = None):
    self.base_url = base_url or os.getenv('FPL_API_BASE_URL')

    if not self.base_url:
      raise ValueError('FPL_API_BASE_URL environment variable is not set')
    
  async def _get(self, endpoint: str) -> dict:
    try:
      async with httpx.AsyncClient() as client:
        response = await client.get(f'{self.base_url}{endpoint}')
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
      print(f'Error fetching data from {endpoint}: {e}')
      raise