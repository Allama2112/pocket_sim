class PlayerState:
    def __init__(self):
        self.active = None
        self.bench = []

        self.deck = []
        self.hand = []
        self.discard = []

        self.energy = 0

        # turn tracking
        self.turns_taken = 0
        self.used_ability_this_turn = set()

class GameState:
    def __init__(self, p1_deck, p2_deck):
        self.players = {
            "p1": PlayerState(),
            "p2": PlayerState()
        }

        self.current_player = "p1"
        self.turn_number = 1
        self.first_player = "p1"

        self.started = False