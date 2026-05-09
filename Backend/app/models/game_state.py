class PlayerState:
    def __init__(self):
        self.active = None
        self.bench = []

        self.deck = []
        self.hand = []
        self.discard = []

        self.stadium = None

        self.energy = 0
        self.turns_taken = 0

        self.supporter_played_this_turn = False
        self.used_ability_this_turn = set()

        self.energy_attached_this_turn = False
        self.has_attacked_this_turn = False
        

class GameState:
    def __init__(self, p1_deck, p2_deck):

        self.players = {
            "p1": PlayerState(),
            "p2": PlayerState()
        }

        self.players["p1"].deck = p1_deck
        self.players["p2"].deck = p2_deck

        self.current_player = "p1"
        self.first_player = "p1"

        self.turn_number = 1
        self.started = False

        # GAME LEVEL
        self.points = {
            "p1": 0,
            "p2": 0
        }

        self.winner = None
        self.game_over = False

        self.turn_phase = "start"
