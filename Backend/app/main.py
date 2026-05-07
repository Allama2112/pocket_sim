from fastapi import FastAPI
from app.api.route_cards import router as cards_router
from app.api.route_decks import router as deck_router   

app = FastAPI()

app.include_router(cards_router)
app.include_router(deck_router)
