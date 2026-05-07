class EffectResolver:
    def __init__(self, effect_registry):
        self.effect_registry = effect_registry

    def resolve(self, game, player_id, card, trigger):
        effects = card.get("effects", [])

        for effect in effects:
            if effect.get("trigger") != trigger:
                continue

            effect_name = effect.get("effect")
            params = effect.get("params", {})

            self.effect_registry.execute(
                effect_name,
                game,
                player_id,
                params
            )

    def resolve_abilities(self, game, player_id, pokemon, trigger):
        abilities = pokemon["card"].get("abilities", [])

        for ability in abilities:
            if ability.get("trigger") != trigger:
                continue

            self.effect_registry.execute(
                ability.get("effect"),
                game,
                player_id,
                ability.get("params", {})
            )
