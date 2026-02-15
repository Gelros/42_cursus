from ex3.CardFactory import CardFactory, Card
from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard

import random


class FantasyCardFactory(CardFactory):
    def __init__(self):
        self.creatures = {
            "dragon": {
                "cost": 5, "rarity": "Legendary", "attack": 7, "health": 5},
            "goblin": {"cost": 2, "rarity": "Common", "attack": 3, "health": 2}
        }
        self.spells = {
            "fireball": {"cost": 3, "rarity": "Rare", "effect_type": "damage"},
            "bolt": {"cost": 3, "rarity": "Rare", "effect_type": "damage"},
        }
        self.artifacts = {
            "mana_ring": {"cost": 2, "rarity": "Uncommon",
                          "durability": 5, "effect": "+1 mana per turn"}
        }

    def create_creature(self, name_or_power: str | int | None = None) -> Card:
        if isinstance(name_or_power, str) and name_or_power in self.creatures:
            key = name_or_power
        else:
            key = random.choice(list(self.creatures.keys()))
        template = self.creatures[key]
        names = {
            "goblin": "Goblin Warrior",
            "dragon": "Fire Dragon"
        }
        return CreatureCard(
            names[key], template["cost"],
            template["rarity"], template["attack"], template["health"])

    def create_spell(self, name_or_power: str | int | None = None) -> Card:
        if isinstance(name_or_power, str) and name_or_power in self.spells:
            key = name_or_power
        else:
            key = random.choice(list(self.spells.keys()))
        template = self.spells[key]
        name = {
            "fireball": "Fireball",
            "bolt": "Lightning Bolt"
        }
        return SpellCard(
            name[key], template["cost"],
            template["rarity"], template["effect_type"]
        )

    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        if isinstance(name_or_power, str) and name_or_power in self.artifacts:
            key = name_or_power
        else:
            key = random.choice(list(self.artifacts.keys()))
        template = self.artifacts[key]
        name = "Mana Ring"
        return ArtifactCard(
            name, template["cost"],
            template["rarity"], template["durability"], template["effect"]
        )

    def create_themed_deck(self, size: int) -> dict:
        deck = []
        create = [self.creatures, self.artifacts, self.spells]

        for i in range(size):
            creator = create[i % len(create)]
            deck.append(creator)

        return {
            "theme": "Fantasy",
            "size": len(deck),
            "cards": deck
        }

    def get_supported_types(self) -> dict:
        return {
            "creatures": list(self.creatures.keys()),
            "spells": list(self.spells.keys()),
            "artifacts": list(self.artifacts.keys())
        }
