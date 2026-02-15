from ex3.FantasyCardFactory import FantasyCardFactory
from ex3.AggressiveStrategy import AgressiveStrategy
from ex3.GameEngine import GameEngine


def main():
    game_engine = GameEngine()
    fantasy = FantasyCardFactory()
    agressive = AgressiveStrategy()

    print("\n=== DataDeck Game Engine ===\n")

    print("Configuring Fantasy Card Game...")
    print("Factory: FantasyCardFactory")
    print("Strategy: AggressiveStrategy")
    print(f"Available types: {fantasy.get_supported_types()}")

    game_engine.configure_engine(fantasy, agressive)
    turn_exec = game_engine.simulate_turn()

    print("\nTurn execution:")
    print(f"Strategy: {agressive.get_strategy_name()}")
    print(f"Actions: {turn_exec['actions']}")

    print("\nGame Report:")
    print(game_engine.get_engine_status())

    print(
        "\nAbstract Factory + Strategy Pattern: Maximum flexibility achieved!")


if __name__ == "__main__":
    main()
