import random
from app.models.game_state import GameState
from app.services.event_engine import EventEngine

class BattleService:
    def __init__(self):
        self.event_engine = EventEngine()

    def create_game(self, p1_deck, p2_deck):
        game = GameState(p1_deck, p2_deck)

        # shuffle decks
        random.shuffle(game.players["p1"].deck)
        random.shuffle(game.players["p2"].deck)

        # draw starting hand (5 cards)
        for _ in range(5):
            self.draw_card(game, "p1")
            self.draw_card(game, "p2")

        game.started = True
        return game

    def draw_card(self, game, player_id):
        player = game.players[player_id]

        if len(player.deck) == 0:
            return

        card = player.deck.pop()
        player.hand.append(card)

    def start_turn(self, game):
        player = game.players[game.current_player]

        # EVENT: turn start
        self.event_engine.emit("on_turn_start", game, {
            "player": game.current_player
        })

        # 1. draw card
        self.draw_card(game, game.current_player)

        # 2. energy rule
        if not (game.turn_number == 1 and game.current_player == game.first_player):
            player.energy += 1

        # 3. reset per-turn flags
        player.used_ability_this_turn = set()

    def end_turn(self, game):
        self.event_engine.emit("on_turn_end", game, {
                "player": game.current_player
            })

        game.current_player = "p2" if game.current_player == "p1" else "p1"
        self.start_turn(game)

battle_service = BattleService()
