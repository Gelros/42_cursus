from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):
    base_rating = 1200

    def __init__(self, name, cost, rarity, attack_power, defense):
        super().__init__(name, cost, rarity)
        self.attack_power = attack_power
        self.defense = defense
        self.rating = self.base_rating
        self.wins = 0
        self.loses = 0
        self.type = "Tournament"

    def play(self, game_state: dict) -> dict:
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Tournament card enters the battlefield"
        }

    def attack(self, target) -> dict:
        target_name = target.name if hasattr(target, 'name') else str(target)
        return {
            "attacker": self.name,
            "target": target_name,
            "damage": self.attack_power,
            "combat_type": "tournament"
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

    def get_combat_stats(self) -> dict:
        return {
            "attack": self.attack_power,
            "defense": self.defense
        }

    def calculate_rating(self) -> int:
        self.rating = self.base_rating + (self.wins * 16) - (self.loses * 16)
        return self.rating

    def update_wins(self, wins: int) -> None:
        self.wins += wins
        self.calculate_rating()

    def update_losses(self, losses: int) -> None:
        self.loses += losses
        self.calculate_rating()

    def get_rank_info(self) -> dict:
        return {
            "name": self.name,
            "rating": self.rating,
            "wins": self.wins,
            "losses": self.loses,
            "record": f"{self.wins}-{self.loses}"
        }
