from ex1.ArtifactCard import ArtifactCard
from ex1.Deck import Deck
from ex1.SpellCard import SpellCard
from ex0.CreatureCard import CreatureCard


def main():
    deck_master = Deck()
    cards = [ArtifactCard, SpellCard, CreatureCard]
    types = [
        ["Mana_cristal", 2, "rare", 2, "+1 mana per turn"],
        ["Fire_bolt", 2, "common", "+2 damage per turn"],
        ["Dragon", 10, "legendary", 50, 100]
    ]
    for card, type_data in zip(cards, types):
        deck_master.add_card(card(*type_data))
    print("\n=== DataDeck Deck Builder ===\n")

    print("Building deck with different card types...")
    print(f"Deck stats: {deck_master.get_deck_stats()}")

    print("\nDrawing and playing cards:")

    len_cards = len(deck_master.cards)
    for _ in range(len_cards):
        drew = deck_master.draw_card()
        print(f"\nDrew: {drew.name} ({drew.type})")
        print(f"{drew.play({})}")

    print(
        "\nPolymorphism in action: Same interface, different card behaviors!")


if __name__ == "__main__":
    main()
