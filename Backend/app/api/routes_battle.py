from fastapi import APIRouter
from pydantic import BaseModel

from app.api import routes_debug
from app.services.battle_service import battle_service

router = APIRouter()


class PlayCardRequest(BaseModel):
    player_id: str
    card_id: str


@router.post("/battle/play-card")
def play_card(data: PlayCardRequest):

    game = routes_debug.test_game

    if game is None:
        return {"error": "No active game"}

    player = game.players[data.player_id]

    # find card in hand
    selected_card = None

    for card in player.hand:
        if card["id"] == data.card_id:
            selected_card = card
            break

    if selected_card is None:
        return {"error": "Card not in hand"}

    result = battle_service.play_card(
        game,
        data.player_id,
        selected_card
    )

    return result