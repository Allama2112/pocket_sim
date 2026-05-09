from fastapi import FastAPI
from app.api.route_cards import router as cards_router
from app.api.route_decks import router as deck_router
from app.api.routes_debug import router as debug_router
from app.services.battle_service import battle_service
from app.api.routes_battle import router as battle_router
from app.api.routes_actions import router as actions_router
from app.api import routes_debug
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cards_router)
app.include_router(deck_router)
app.include_router(debug_router)
app.include_router(battle_router)
app.include_router(actions_router)

sample_pokemon = {
    "id": "a1-001",
    "name": "Bulbasaur",
    "type": "Pokemon",
    "health": 70,
    "attacks": [
        {
            "name": "Vine Whip",
            "damage": "40",
            "cost": ["Grass"]
        }
    ]
}

p1_deck = [sample_pokemon.copy() for _ in range(20)]
p2_deck = [sample_pokemon.copy() for _ in range(20)]

routes_debug.test_game = battle_service.create_game(
    p1_deck,
    p2_deck
)
