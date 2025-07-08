from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_cards
from app.api.routes_cards import router as cards_router

from app.db import create_db_and_tables

if __name__ == "__main__":
	create_db_and_tables()

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(cards_router)

