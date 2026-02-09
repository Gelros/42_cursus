import alchemy
from alchemy.elements import create_water, create_fire, create_earth
from alchemy.potions import healing_potion as heal
from alchemy.potions import strength_potion


def main():
    print("\n=== Import Transmutation Mastery ===")

    print("\nMethod 1 - Full module import:")
    fire = alchemy.elements.create_fire()
    print(f"alchemy.elements.create_fire(): {fire}")

    print("\nMethod 2 - Specific function import:")
    print(f"create_water(): {create_water()}")

    print("\nMethod 3 - Aliased import:")
    print(f"heal(): {heal()}")

    print("\nMethod 4 - Multiple imports:")
    print(f"create_earth(): {create_earth()}")
    print(f"create_fire(): {create_fire()}")
    print(f"strength_potion(): {strength_potion()}")

    print("\nAll import transmutation methods mastered!")


if __name__ == "__main__":
    main()
