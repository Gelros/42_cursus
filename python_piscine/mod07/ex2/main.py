from ex2.EliteCard import EliteCard
from ex2.Combatable import Combatable
from ex2.Magical import Magical
from ex0.Card import Card


def main():

    print("\n=== DataDeck Ability System ===\n")

    print("EliteCard capabilities:")
    class_lst = [Card, Magical, Combatable]
    for i in class_lst:
        methodes = [m for m in dir(i) if not m.startswith('_')]
        print(f"- {i.__name__}: {methodes}")

    elite = EliteCard("arcane_warrior", 5, "rare", 12, 7, 20)
    ennemy = ["enemy 1", "enemy 2"]

    print("\nPlaying Arcane Warrior (Elite Card):\n")

    print("Combat phase:")
    print(f"Attack result: {elite.attack("Dragon")}")
    print(f"Defense result: {elite.defend(4)}")

    print("\nMagic phase:")
    print(f"Spell cast: {elite.cast_spell("Fireball", ennemy)}")
    print(f"Mana chanel: {elite.channel_mana(3)}")

    print("\nMultiple interface implementation successful!")


if __name__ == "__main__":
    main()
