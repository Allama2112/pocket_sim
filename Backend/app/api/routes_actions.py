from fastapi import APIRouter
from pydantic import BaseModel

from app.api import routes_debug
from app.services.battle_service import battle_service

router = APIRouter()


class AttackRequest(BaseModel):
    player_id: str
    attack_index: int = 0


class EndTurnRequest(BaseModel):
    player_id: str


@router.post("/battle/attack")
def attack(data: AttackRequest):
    game = routes_debug.test_game

    if game is None or game.game_over:
        return {"error": "Game not active"}

    return battle_service.attack(
        game,
        data.player_id,
        data.attack_index
    )


@router.post("/battle/end-turn")
def end_turn(data: EndTurnRequest):
    game = routes_debug.test_game

    if game is None or game.game_over:
        return {"error": "Game not active"}

    battle_service.end_turn(game)

    return {
        "message": "Turn ended",
        "current_player": game.current_player
    }