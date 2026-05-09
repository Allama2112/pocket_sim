from fastapi import APIRouter
from app.services.battle_service import battle_service

router = APIRouter()

test_game = None

@router.get("/debug/game")
def get_game():
    global test_game

    return test_game