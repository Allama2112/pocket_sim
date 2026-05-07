from pydantic import BaseModel
from typing import List

class Deck(BaseModel):
    id: str
    cards: List[str]  # list of card IDs