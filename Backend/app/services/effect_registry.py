class EffectRegistry:
    def __init__(self):
        self.effects = {}

    def register(self, name, handler):
        self.effects[name] = handler

    def execute(self, name, game, player_id, params=None):
        if name not in self.effects:
            return {"error": f"Unknown effect: {name}"}

        return self.effects[name](game, player_id, params or {})
    