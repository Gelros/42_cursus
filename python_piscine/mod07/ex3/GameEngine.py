from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:
    def __init__(self):
        self.factory = None
        self.strategy = None
        self.hand = []
        self.battlefield = []
        self.turns_simulated = 0
        self.total_damage = 0
        self.cards_created = 0

    def configure_engine(
            self, factory: CardFactory, strategy: GameStrategy) -> None:
        self.factory = factory
        self.strategy = strategy

        dragon = self.factory.create_creature("dragon")
        goblin = self.factory.create_creature("goblin")
        spell = self.factory.create_spell("fireball")

        self.hand = [dragon, goblin, spell]
        self.cards_created = len(self.hand)

    def simulate_turn(self) -> dict:
        if not self.factory or not self.strategy:
            return {"error": "Engine not configured"}

        print("\nSimulating aggressive turn...")
        hand_display = [f"{card.name} ({card.cost})" for card in self.hand]
        print(f"Hand: {hand_display}")

        turn = self.strategy.execute_turn(self.hand, self.battlefield)
        self.turns_simulated += 1
        total = turn["actions"]["damage_dealt"]
        self.total_damage += total

        return turn

    def get_engine_status(self) -> dict:
        return {
            "turns_simulated": self.turns_simulated,
            "strategy_used": self.strategy.get_strategy_name(),
            "total_damage": self.total_damage,
            "cards_created": self.cards_created
        }
