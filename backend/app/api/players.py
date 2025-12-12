from typing import List
from fastapi import APIRouter, Depends

from app.services.fpl_service import FPLService, get_fpl_service
from backend.app.models.dtos.player_dto import PlayerDTO
from backend.app.models.mappers.player_mapper import map_raw_player_to_dto

router = APIRouter(
  prefix='/players',
)

@router.get('/', response_model=List[PlayerDTO])
async def get_players(fpl_service: FPLService = Depends(get_fpl_service)) -> List[PlayerDTO]:
  """ Retrieve all players from fpl endpoint and convert to player dto for frontemnd

  Args:
      fpl_service (FPLService, optional): FPL service class containing all required methods

  Returns:
      list: Return a list of all players as PlayerDTO objects
  """

  players = await fpl_service.get_all_players()

  return players

@router.get('/{player_id}')
async def get_player_details(
  player_id: int,
  fpl_service: FPLService = Depends(get_fpl_service)
) -> dict:
  """ Get details for a specific player

  Args:
      player_id (int): Player id as defined in FPL API
      fpl_service (FPLService, optional): FPL service class containing all required methods

  Returns:
      dict: Return a dictionary containing player details
  """

  player_details = await fpl_service.fetch_player_details(player_id)
  return player_details

@router.get('/{player_id}/fixtures')
async def get_player_fixtures(
  player_id: int,
  fpl_service: FPLService = Depends(get_fpl_service)
) -> List[dict]:
  """ Get list of fixtures for a specific player

  Args:
    player_id (int): Player id as defined in FPL API
    fpl_service (FPLService, optional): FPL service class containing all required methods

  Returns:
    List[dict]: Return list of fixtures and data related to each fixture
  """

  player_fixtures = await fpl_service.fetch_player_fixtures(player_id)
  return player_fixtures


