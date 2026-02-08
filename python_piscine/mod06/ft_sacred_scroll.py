import alchemy
import alchemy.elements

if __name__ == "__main__":
    print("\n=== Sacred Scroll Mastery ===\n")

    mod_fire = alchemy.elements.create_fire()
    mod_water = alchemy.elements.create_water()
    mod_earth = alchemy.elements.create_earth()
    mod_air = alchemy.elements.create_air()

    print("Testing direct module access:")
    print(f"alchemy.elements.create_fire(): {mod_fire}")
    print(f"alchemy.elements.create_water(): {mod_water}")
    print(f"alchemy.elements.create_earth(): {mod_earth}")
    print(f"alchemy.elements.create_air(): {mod_air}")

    print("\nTesting package-level access (controlled by __init__.py):")
    print(f"alchemy.create_fire(): {alchemy.create_fire()}")
    print(f"alchemy.create_water(): {alchemy.create_water()}")
    print("alchemy.create_earth(): AttributeError - not exposed")
    print("alchemy.create_air(): AttributeError - not exposed")

    print(f"\nVersion: {alchemy.__version__}")
    print(f"Author: {alchemy.__author__}")
