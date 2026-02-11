from ex0.CreatureCard import CreatureCard


def main():
    dragon = CreatureCard("Dragon", 6, "legendary", 15, 50)
    goblin = CreatureCard("Goblin", 2, "common", 2, 15)

    print("\n=== DataDeck Card Foundation ===\n")

    print(f"CreatureCard Info:\n{dragon.get_card_info()}")

    print(f"\nPlaying {dragon.name} with 6 mana available:")
    print(f"Playable: {dragon.is_playable(6)}")
    print(f"Play result: {dragon.play({})}")

    print("\nFire Dragon attacks Goblin Warrior:")
    print(f"Attack result: {dragon.attack_target(goblin)}")

    print("\nTesting insufficient mana (3 available)")
    print(f"Playable: {dragon.is_playable(3)}")

    print("\nAbstract pattern successfully demonstrated!")


if __name__ == "__main__":
    main()
