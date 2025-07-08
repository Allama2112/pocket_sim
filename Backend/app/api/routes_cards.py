from fastapi import APIRouter
from app.models.card import Card, Attack

router = APIRouter()

# Fake in-memory card list (eventually from Supabase)
cards_db = [
    Card(
        id="001",
        name="Pikachu",
        type="pokemon",
        hp=60,
        attacks=[Attack(name="Thunder Shock", damage=20, cost=["lightning"])],
        description="An electric mouse Pokémon."
    ),
    Card(
        id="002",
        name="Potion",
        type="trainer",
        description="Heal 30 damage from one of your Pokémon."
    ),
    Card(
        id="003",
        name="Lightning Energy",
        type="energy",
        description="Provides ⚡ energy."
    ),
]


@router.get("/", response_model=list[Card])
def get_all_cards():
    return cards_db
