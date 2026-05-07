from fastapi import APIRouter
from app.services.battle_service import battle_service

router = APIRouter()

@router.get("/game/status")
def game_status(game):
    return {
        "winner": game.winner,
        "game_over": game.game_over,
        "current_player": game.current_player
    }