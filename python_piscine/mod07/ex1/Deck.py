from ex0.Card import Card
import random


class Deck:
    def __init__(self):
        self.cards = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def remove_card(self, card_name: str) -> bool:
        for i, card in enumerate(self.cards):
            if card.name == card_name:
                self.cards.pop(i)
                return True
        return False

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        return self.cards.pop(0)

    def get_deck_stats(self) -> dict:
        n_creature = sum(
            1 for i in self.cards if getattr(i, "type", None) == "Creature")
        n_spell = sum(
            1 for i in self.cards if getattr(i, "type", None) == "Spell")
        n_artifact = sum(
            1 for i in self.cards if getattr(i, "type", None) == "Artifact")
        avg = sum(i.cost for i in self.cards) / len(self.cards)

        return {
            "total_cards": len(self.cards),
            "creatures": n_creature,
            "spells": n_spell,
            "artifacts": n_artifact,
            "avg_cost": f"{avg:.1f}"
        }
