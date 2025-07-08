from pydantic import BaseModel
from typing import Optional, List


class Attack(BaseModel):
    name: str
    damage: Optional[int] = 0
    cost: Optional[List[str]] = []


class Card(BaseModel):
    id: str
    name: str
    type: str  # 'pokemon', 'trainer', 'energy'
    hp: Optional[int] = None
    attacks: Optional[List[Attack]] = None
    description: Optional[str] = None
    image_url: Optional[str] = None  # For later if you want to use images
