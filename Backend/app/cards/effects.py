def draw_card_effect(game, context):
    player_id = context["player"]
    player = game.players[player_id]

    if len(player.deck) > 0:
        card = player.deck.pop()
        player.hand.append(card)