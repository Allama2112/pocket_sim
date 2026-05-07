from collections import defaultdict

class DeckService:
    def __init__(self):
        self.decks = {}

    def create_deck(self, deck_id: str):
        if deck_id in self.decks:
            return {"error": "Deck already exists"}

        self.decks[deck_id] = []
        return {"message": "Deck created", "deck_id": deck_id}

    def add_card(self, deck_id: str, card_id: str):
        if deck_id not in self.decks:
            return {"error": "Deck not found"}

        self.decks[deck_id].append(card_id)
        return {"message": "Card added"}

    def get_deck(self, deck_id: str):
        return self.decks.get(deck_id, {"error": "Deck not found"})

    def validate_deck(self, deck_id: str):
        deck = self.decks.get(deck_id)

        if not deck:
            return {"error": "Deck not found"}

        if len(deck) != 20:
            return {"valid": False, "reason": "Deck must be 20 cards"}

        return {"valid": True}

deck_service = DeckService()