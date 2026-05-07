class PlayerState:
    def __init__(self):
        self.active = None
        self.bench = []

        self.deck = []
        self.hand = []
        self.discard = []

        self.points = {
            "p1": 0,
            "p2": 0
        }

        self.winner = None
        self.game_over = False

        # Pocket systems
        self.stadium = None

        self.energy = 0

        # turn tracking
        self.turns_taken = 0

        self.supporter_played_this_turn = False
        self.used_ability_this_turn = set()

        self.winner = None
        self.game_over = False

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