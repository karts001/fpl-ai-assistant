from fastapi import APIRouter, Depends, HTTPException

from backend.app.models.requests.transfer_suggestion import TransferSuggestionRequest
from backend.app.services.ai_service import AIService, get_ai_service
from backend.app.services.fpl_service import FPLService, get_fpl_service


router = APIRouter()

@router.post('/suggest-transfers')
async def suggest_transfers(
  request: TransferSuggestionRequest,
  ai_service: AIService = Depends(get_ai_service),
  fpl_service: FPLService = Depends(get_fpl_service)
):
  try:
    players = await fpl_service.get_all_players()

    result = await ai_service.suggest_transfers(
      budget=request.budget,
      position=request.position,
      players=players,
      num_recommendations=request.num_recommendations
    )

    return result
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))