def draw_card(game, player_id, params):
    player = game.players[player_id]

    if len(player.deck) == 0:
        return

    card = player.deck.pop()
    player.hand.append(card)


def heal_damage(game, player_id, params):
    amount = params.get("amount", 0)

    player = game.players[player_id]

    if player.active:
        player.active["damage"] = max(
            0,
            player.active["damage"] - amount
        )


def search_basic_pokemon(game, player_id, params):
    # placeholder logic for later refinement
    pass