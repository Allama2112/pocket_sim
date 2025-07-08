from fastapi import APIRouter, HTTPException
from typing import List
from app.models.card import Card

router = APIRouter()

# Simulate a DB with a list
cards_db: List[Card] = []

@router.get("/cards", response_model=List[Card])
def get_cards():
    return cards_db

@router.get("/cards/{card_id}", response_model=Card)
def get_card(card_id: int):
    for card in cards_db:
        if card.id == card_id:
            return card
    raise HTTPException(status_code=404, detail="Card not found")

@router.post("/cards", response_model=Card)
def create_card(card: Card):
    # Check if card with same id exists
    if any(c.id == card.id for c in cards_db):
        raise HTTPException(status_code=400, detail="Card ID already exists")
    cards_db.append(card)
    return card
