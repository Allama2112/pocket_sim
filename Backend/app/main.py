from fastapi import FastAPI
from app.api.route_cards import router as cards_router

app = FastAPI()

app.include_router(cards_router)