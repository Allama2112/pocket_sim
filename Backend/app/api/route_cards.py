from fastapi import APIRouter, Query
from app.services.card_service import card_service

router = APIRouter()

@router.get("/cards")
def get_cards():
    return card_service.get_all_cards()

# Search cards
@router.get("/cards/search")
def search_cards(name: str):
    return card_service.search_cards(name)

# Get single card by id
@router.get("/cards/{card_id}")
def get_card(card_id: str):
    card = card_service.get_card_by_id(card_id)

    if not card:
        return {"error": "Card not found"}

    return card

