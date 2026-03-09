from ex4.TournamentCard import TournamentCard
from ex4.TournamentPlatform import TournamentPlatform


def main():

    print("\n=== DataDeck Tournament Platform ===\n")

    print("Registering Tournament Cards...")
    manager = TournamentPlatform()
    cards = [
        TournamentCard("dragon", 5, "rare", 50, 300),
        TournamentCard("goblin", 3, "common", 3, 30)
    ]

    id_001 = manager.register_card(cards[0])
    id_002 = manager.register_card(cards[1])
    match_res = manager.create_match(id_001, id_002)
    leaderboard = manager.get_leaderboard()

    for card in cards:
        card_info = card.get_rank_info()
        print(f"\n{card.name} ({manager.register_card(card)}):")
        print("- Interfaces: [Card, Combatable, Rankable]")
        print(f"- Rating: {card.rating}")
        print(f"- Record: {card_info["record"]}")

    print("\nCreating tournament match...")
    print(f"Match result: {match_res}")

    print("\nTournament Leaderboard:")
    i = 1
    for lead in leaderboard:
        print(
            f"{i}. {lead["name"]} - Rating: {lead["rating"]} "
            f"({lead["record"]})"
            )
        i += 1

    print("\nPlatform Report:")
    print(manager.generate_tournament_report())

    print(
        "\n=== Tournament Platform Successfully Deployed! ===\n"
        "All abstract patterns working together harmoniously!"
        )


if __name__ == "__main__":
    main()
