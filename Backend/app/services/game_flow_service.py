class GameFlowService:

    def check_win(self, game):
        for player_id, player in game.players.items():

            opponent_id = "p2" if player_id == "p1" else "p1"
            opponent = game.players[opponent_id]

            # WIN CONDITION 1: no board presence
            if opponent.active is None and len(opponent.bench) == 0:
                game.game_over = True
                game.winner = player_id
                return True

        return False

