import random
from app.models.game_state import GameState
from app.services.event_engine import EventEngine
from app.services.effect_registry import EffectRegistry
from app.services.effect_resolver import EffectResolver
from app.services.game_flow_service import GameFlowService
from app.cards.effects_impl import draw_card, heal_damage


class BattleService:
    def __init__(self):
        self.event_engine = EventEngine()

        self.effect_registry = EffectRegistry()
        self.effect_registry.register("draw_card", draw_card)
        self.effect_registry.register("heal_damage", heal_damage)

        self.effect_resolver = EffectResolver(self.effect_registry)

        self.game_flow = GameFlowService()

    # =========================
    # GAME SETUP
    # =========================

    def create_game(self, p1_deck, p2_deck):
        game = GameState(p1_deck, p2_deck)

        random.shuffle(game.players["p1"].deck)
        random.shuffle(game.players["p2"].deck)

        for _ in range(5):
            self.draw_card(game, "p1")
            self.draw_card(game, "p2")

        game.started = True
        return game

    # =========================
    # CARD DRAW
    # =========================

    def draw_card(self, game, player_id):
        player = game.players[player_id]

        if len(player.deck) == 0:
            return

        card = player.deck.pop()

        if card is None:
            return
        player.hand.append(card)

    # =========================
    # CARD PLAY DISPATCHER
    # =========================

    def play_card(self, game, player_id, card, **kwargs):
        card_type = card.get("type")

        if game.game_over:
            return {"error": "Game is over"}

        if card_type == "Pokemon":
            return self.play_pokemon(game, player_id, card)

        if card_type == "Item":
            return self.play_item(game, player_id, card)

        if card_type == "Supporter":
            return self.play_supporter(game, player_id, card)

        if card_type == "Stadium":
            return self.play_stadium(game, player_id, card)

        if card_type == "Tool":
            return self.play_tool(
                game,
                player_id,
                card,
                kwargs.get("target_slot"),
                kwargs.get("target_index"),
            )

        return {"error": "Unknown card type"}

    # =========================
    # POKEMON PLAY
    # =========================

    def play_pokemon(self, game, player_id, card):
        player = game.players[player_id]

        placement = None

        if player.active is None:
            player.active = {
                "card": card,
                "damage": 0,
                "energy": 0,
                "turn_played": game.turn_number,
                "tool": None,
                "evolved_this_turn": False
            }
            placement = "active"

        elif len(player.bench) < 3:
            player.bench.append({
                "card": card,
                "damage": 0,
                "energy": 0,
                "turn_played": game.turn_number,
                "tool": None,
                "evolved_this_turn": False
            })
            placement = "bench"

        else:
            return {"error": "Bench full"}

        for i, c in enumerate(player.hand):
            if c.get("id") == card.get("id"):
                player.hand.pop(i)
                break

        self.event_engine.emit("on_play_pokemon", game, {
            "player": player_id,
            "card": card,
            "placement": placement
        })

        self.effect_resolver.resolve(
            game,
            player_id,
            card,
            "on_play_pokemon"
        )

        return {
            "message": "Pokemon played",
            "placement": placement
        }

    # =========================
    # SUPPORTER PLAY
    # =========================

    def play_supporter(self, game, player_id, card):
        player = game.players[player_id]

        if player.supporter_played_this_turn:
            return {"error": "Supporter already played this turn"}
        
        if game.turn_phase != "main":
            return {"error": "Cannot play supporter outside main phase"}

        player.supporter_played_this_turn = True
        player.hand.remove(card["id"])

        self.event_engine.emit("on_play_supporter", game, {
            "player": player_id,
            "card": card
        })

        self.effect_resolver.resolve(
            game,
            player_id,
            card,
            "on_play_supporter"
        )

        player.discard.append(card["id"])
        return {"message": "Supporter played"}

    # =========================
    # ITEM PLAY
    # =========================

    def play_item(self, game, player_id, card):
        player = game.players[player_id]

        player.hand.remove(card["id"])

        self.event_engine.emit("on_play_item", game, {
            "player": player_id,
            "card": card
        })

        self.effect_resolver.resolve(
            game,
            player_id,
            card,
            "on_play_item"
        )

        player.discard.append(card["id"])
        return {"message": "Item played"}

    # =========================
    # STADIUM PLAY
    # =========================

    def play_stadium(self, game, player_id, card):
        player = game.players[player_id]

        if player.stadium:
            player.discard.append(player.stadium["id"])

        player.stadium = card
        player.hand.remove(card["id"])

        self.event_engine.emit("on_play_stadium", game, {
            "player": player_id,
            "card": card
        })

        return {"message": "Stadium played"}

    # =========================
    # TOOL PLAY
    # =========================

    def play_tool(self, game, player_id, card, target_slot, target_index=None):
        player = game.players[player_id]

        if target_slot == "active":
            target = player.active
        elif target_slot == "bench":
            if target_index is None:
                return {"error": "Bench index required"}

            if target_index >= len(player.bench):
                return {"error": "Invalid bench index"}

            target = player.bench[target_index]
        else:
            return {"error": "Invalid target slot"}

        if target is None:
            return {"error": "No pokemon in target slot"}

        if target["tool"] is not None:
            return {"error": "Pokemon already has a tool"}

        target["tool"] = card
        player.hand.remove(card["id"])

        self.event_engine.emit("on_attach_tool", game, {
            "player": player_id,
            "card": card,
            "target": target
        })

        return {"message": "Tool attached"}

    # =========================
    # TURN SYSTEM
    # =========================

    def reset_turn_flags(self, player):
        if player.active:
            player.active["evolved_this_turn"] = False

        for p in player.bench:
            p["evolved_this_turn"] = False

    def start_turn(self, game):
        player = game.players[game.current_player]

        self.reset_turn_flags(player)

        game.turn_phase = "start"

        self.event_engine.emit("on_turn_start", game, {
            "player": game.current_player
        })

        # draw phase
        self.draw_card(game, game.current_player)

        # energy rule (first turn exception already handled)
        if not (game.turn_number == 1 and game.current_player == game.first_player):
            player.energy += 1

        player.energy_attached_this_turn = False
        player.has_attacked_this_turn = False

        player.supporter_played_this_turn = False
        player.used_ability_this_turn = set()

        game.turn_phase = "main"

    def end_turn(self, game):
        self.event_engine.emit("on_turn_end", game, {
            "player": game.current_player
        })

        self.resolve_stadium(game, "on_turn_end")
        self.resolve_all_abilities(game, "on_turn_end")

        game.current_player = (
            "p2" if game.current_player == "p1" else "p1"
        )

        self.check_win(game)

        self.start_turn(game)

        game.turn_phase = "end"

    # =========================
    # ATTACK SYSTEM
    # =========================

    def attack(self, game, player_id, attack_index=0):
        player = game.players[player_id]

        if game.game_over:
            return {"error": "Game is over"}

        if player.active is None:
            return {"error": "No active pokemon"}
        
        if player.has_attacked_this_turn:
            return {"error": "Already attacked this turn"}

        attacker = player.active
        defender_id = "p2" if player_id == "p1" else "p1"
        defender = game.players[defender_id]

        if defender.active is None:
            return {"error": "Opponent has no active pokemon"}

        attack_data = attacker["card"]["attacks"][attack_index]

        attack_cost = len(attack_data.get("cost", []))

        if player.energy < attack_cost:
            return {"error": "Not enough energy"}

        damage = self.parse_damage(attack_data.get("damage", "0"))

        # BEFORE ATTACK
        self.event_engine.emit("before_attack", game, {
            "attacker": attacker,
            "defender": defender.active,
            "damage": damage
        })

        self.effect_resolver.resolve(
            game,
            player_id,
            attacker["card"],
            "before_attack"
        )

        self.resolve_stadium(game, "before_attack")
        self.resolve_all_abilities(game, "before_attack")

        # APPLY DAMAGE FIRST
        defender.active["damage"] += damage

        # DAMAGE TRIGGERS (AFTER APPLY)
        self.effect_resolver.resolve(
            game,
            defender_id,
            defender.active["card"],
            "on_damage_taken"
        )

        self.resolve_all_abilities(game, "on_damage_taken")
        self.resolve_stadium(game, "on_damage_taken")

        # AFTER ATTACK
        self.event_engine.emit("after_attack", game, {
            "attacker": attacker,
            "defender": defender.active,
            "damage": damage
        })

        self.effect_resolver.resolve(
            game,
            player_id,
            attacker["card"],
            "after_attack"
        )

        self.resolve_stadium(game, "after_attack")
        self.resolve_all_abilities(game, "after_attack")

        self.check_knockout(game, defender_id)

        self.game_flow.check_win(game)

        player.has_attacked_this_turn = True

        return {
            "message": "Attack successful",
            "damage": damage
        }

    def parse_damage(self, damage_text):
        digits = ""
        for c in damage_text:
            if c.isdigit():
                digits += c
        return int(digits) if digits else 0

    # =========================
    # KO SYSTEM
    # =========================

    def check_knockout(self, game, player_id):
        player = game.players[player_id]

        if player.active is None:
            return

        pokemon = player.active

        hp = pokemon["card"]["health"]
        damage = pokemon["damage"]

        if damage < hp:
            return

        knocked_out = pokemon

        # ---- POINT SYSTEM ----
        # default 1 point per KO
        points_awarded = 1

        # OPTIONAL: rarity scaling example
        rarity = knocked_out["card"].get("rarity", "Common")

        if rarity == "Rare":
            points_awarded = 2
        elif rarity == "Ultra Rare":
            points_awarded = 3

        self.add_points(game, player_id, points_awarded)

        # move to discard
        player.discard.append(knocked_out["card"]["id"])

        if knocked_out["tool"]:
            player.discard.append(knocked_out["tool"]["id"])

        player.active = None

        self.event_engine.emit("on_knockout", game, {
            "player": player_id,
            "pokemon": knocked_out,
            "points": points_awarded
        })

        # check if game ended after KO
        self.check_game_over(game)

    def check_win(self, game):
        p1 = game.points["p1"]
        p2 = game.points["p2"]

        p1_board = game.players["p1"]
        p2_board = game.players["p2"]

        # Board loss condition
        if p1_board.active is None and len(p1_board.bench) == 0:
            game.winner = "p2"
            game.game_over = True
            return

        if p2_board.active is None and len(p2_board.bench) == 0:
            game.winner = "p1"
            game.game_over = True
            return

        # 🏁 POINT WIN CONDITION
        if p1 >= 3 or p2 >= 3:

            # simultaneous reach check
            if p1 >= 3 and p2 >= 3:

                if p1 > p2:
                    game.winner = "p1"
                elif p2 > p1:
                    game.winner = "p2"
                else:
                    game.winner = "draw"

                game.game_over = True
                return

            if p1 >= 3:
                game.winner = "p1"
                game.game_over = True
                return

            if p2 >= 3:
                game.winner = "p2"
                game.game_over = True
                return

    # =========================
    # EVOLUTION SYSTEM
    # =========================

    def evolve_pokemon(
        self,
        game,
        player_id,
        evolution_card,
        target_slot,
        target_index=None
    ):
        player = game.players[player_id]

        if target_slot == "active":
            target = player.active
        elif target_slot == "bench":
            if target_index is None:
                return {"error": "Bench index required"}

            if target_index >= len(player.bench):
                return {"error": "Invalid bench index"}
            target = player.bench[target_index]
        else:
            return {"error": "Invalid target slot"}

        if target is None:
            return {"error": "No pokemon found"}

        base = target["card"]

        if evolution_card.get("evolvesFrom") != base.get("name"):
            return {"error": "Invalid evolution"}

        if game.turn_number < target["turn_played"] + 2:
            return {"error": "Too early to evolve"}

        if target["evolved_this_turn"]:
            return {"error": "Already evolved this turn"}

        target["card"] = evolution_card
        target["evolved_this_turn"] = True

        player.hand.remove(evolution_card["id"])

        self.event_engine.emit("on_evolve", game, {
            "player": player_id,
            "from": base,
            "to": evolution_card
        })

        return {"message": "Pokemon evolved"}

    # =========================
    # HELPERS
    # =========================

    def resolve_stadium(self, game, trigger):
        for pid, player in game.players.items():
            if player.stadium:
                self.effect_resolver.resolve(
                    game,
                    pid,
                    player.stadium,
                    trigger
                )

    def resolve_all_abilities(self, game, trigger):
        for pid, player in game.players.items():

            if player.active:
                self.effect_resolver.resolve_abilities(
                    game,
                    pid,
                    player.active,
                    trigger
                )

            for p in player.bench:
                self.effect_resolver.resolve_abilities(
                    game,
                    pid,
                    p,
                    trigger
                )

    def attach_energy(self, game, player_id, target_slot, target_index=None):
        player = game.players[player_id]

        if game.game_over:
            return {"error": "Game is over"}

        if player.energy <= 0:
            return {"error": "No energy available"}

        if player.energy_attached_this_turn:
            return {"error": "Energy already attached this turn"}

        # locate target
        if target_slot == "active":
            target = player.active
        else:
            if target_index is None:
                return {"error": "Missing bench index"}
            target = player.bench[target_index]

        if target is None:
            return {"error": "No target Pokémon"}

        # attach (simple version)
        target.setdefault("energy", 0)
        target["energy"] += 1

        player.energy -= 1
        player.energy_attached_this_turn = True

        return {"message": "Energy attached"}
    
    def add_points(self, game, player_id, amount):
        game.points[player_id] += amount

        # check win condition immediately
        if game.points[player_id] >= 3:
            self.check_game_over(game)


    def check_game_over(self, game):
        p1 = game.points["p1"]
        p2 = game.points["p2"]

        # both hit 3+
        if p1 >= 3 and p2 >= 3:
            if p1 > p2:
                game.winner = "p1"
            elif p2 > p1:
                game.winner = "p2"
            else:
                game.winner = "draw"

            game.game_over = True
            return

        # single winner
        if p1 >= 3:
            game.winner = "p1"
            game.game_over = True
            return

        if p2 >= 3:
            game.winner = "p2"
            game.game_over = True
            return

        # deck loss condition (optional rule you already had)
        if len(game.players["p1"].deck) == 0 and len(game.players["p1"].hand) == 0:
            game.winner = "p2"
            game.game_over = True

        if len(game.players["p2"].deck) == 0 and len(game.players["p2"].hand) == 0:
            game.winner = "p1"
            game.game_over = True


# global instance
battle_service = BattleService()