from ex2.Combatable import Combatable
from ex2.Magical import Magical
from ex0.Card import Card


class EliteCard(Card, Magical, Combatable):
    def __init__(
            self, name: str, cost: int, rarity: str,
            attack_power: int, defense: int, mana_pool: int):
        super().__init__(name, cost, rarity)
        self.attack_power = attack_power
        self.defense = defense
        self.mana_pool = mana_pool
        self.type = "Elite Card"

    def play(self, game_state: dict) -> dict:
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Elite card deployed with combat magic abilities"
        }

    def get_magic_stats(self) -> dict:
        return {"mana_pool": self.mana_pool}

    def channel_mana(self, amount: int) -> dict:
        self.mana_pool += amount
        return {
            "channeled": amount,
            "total_mana": self.mana_pool
        }

    def cast_spell(self, spell_name: str, targets: list) -> dict:
        return {
            "caster": self.name,
            "spell": spell_name,
            "targets": targets,
            "mana_used": self.cost
        }

    def get_combat_stats(self) -> dict:
        return {
            "attack": self.attack_power,
            "defense": self.defense
        }

    def defend(self, incoming_damage: int) -> dict:
        atk = incoming_damage
        defense = self.defense
        damage_taken = atk - defense if atk > defense else 0
        still_alive = False if damage_taken > 0 else True
        return {
            "defender": self.name,
            "damage_taken": damage_taken,
            "damage_blocked": defense if atk > defense else atk,
            "still_alive": still_alive
        }

    def attack(self, target: str) -> dict:
        return {
            "attacker": self.name,
            "target": target,
            "damage": self.attack_power,
            "combat_type": "melee"
        }
