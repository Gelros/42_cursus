from ex0.Card import Card


class CreatureCard(Card):
    def __init__(
     self, name: str, cost: int, rarity: str, attack: int, health: int):
        super().__init__(name, cost, rarity)
        self.attack = attack
        self.health = health
        self.type = "Creature"

    def play(self, game_state: dict) -> dict:
        res = {
            "card_player": self.name,
            "mana_used": self.cost,
            "effect": "Creature summoned to battlefield"
        }
        return res

    def attack_target(self, target: dict) -> dict:
        is_dead = False
        if self.attack > target.health:
            is_dead = True
        res = {
            "attacker": self.name,
            "target": target.name,
            "dama_dealt": self.attack,
            "combat_resolve": is_dead
        }
        return res
