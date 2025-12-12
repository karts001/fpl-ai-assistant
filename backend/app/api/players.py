from typing import List
from fastapi import APIRouter, Depends

from app.services.fpl_service import FPLService, get_fpl_service
from backend.app.models.dtos.player_dto import PlayerDTO
from backend.app.models.mappers.player_mapper import map_raw_player_to_dto

router = APIRouter(
    prefix='/players',
)

@router.get('/')
async def get_players(fpl_service: FPLService = Depends(get_fpl_service)) -> List[PlayerDTO]:
  """ Retrieve all players from fpl endpoint and convert to player dto for frontemnd

  Args:
      fpl_service (FPLService, optional): FPL service class containing all required methods

  Returns:
      list: Return a list of all players as PlayerDTO objects
  """

  raw_players = await fpl_service.fetch_all_players()

  players = [map_raw_player_to_dto(p) for p in raw_players]
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


