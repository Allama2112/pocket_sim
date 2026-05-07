import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CARDS_DIR = BASE_DIR / "data" / "cards" / "cards" / "en"

class CardService:
    def __init__(self):
        self.cards = self.load_cards()

        # Index
        self.cards_by_id = {
            card.get("id"): card
            for card in self.cards
            if "id" in card
        }

    def load_cards(self):
        all_cards = []

        json_files = list(CARDS_DIR.glob("*.json"))

        for file_path in json_files:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                if isinstance(data, list):
                    all_cards.extend(data)

                elif isinstance(data, dict):
                    for key in ["data", "cards", "results"]:
                        if key in data and isinstance(data[key], list):
                            all_cards.extend(data[key])
                            break

        return all_cards

    def get_all_cards(self):
        return self.cards

    # Get by id
    def get_card_by_id(self, card_id):
        return self.cards_by_id.get(card_id)

    # Search by name
    def search_cards(self, name: str):
        print("SEARCH CALLED WITH:", name)

        name = name.lower()

        results = [
            card for card in self.cards
            if name in card.get("name", "").lower()
        ]

        print("RESULTS FOUND:", len(results))

        return results


card_service = CardService()
