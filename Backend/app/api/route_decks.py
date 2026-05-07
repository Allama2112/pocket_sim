from fastapi import APIRouter
from app.services.deck_service import deck_service

router = APIRouter()

@router.post("/deck/create")
def create_deck(deck_id: str):
    return deck_service.create_deck(deck_id)


@router.post("/deck/{deck_id}/add")
def add_card(deck_id: str, card_id: str):
    return deck_service.add_card(deck_id, card_id)


@router.get("/deck/{deck_id}")
def get_deck(deck_id: str):
    return deck_service.get_deck(deck_id)


@router.get("/deck/{deck_id}/validate")
def validate_deck(deck_id: str):
    return deck_service.validate_deck(deck_id)