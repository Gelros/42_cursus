import alchemy
import alchemy.elements


def healing_potion() -> str:
    fire = alchemy.create_fire()
    water = alchemy.create_water()
    return f"Healing potion brewed with {fire} and {water}"


def  strength_potion() -> str:
    earth = alchemy.elements.create_earth()
    fire = alchemy.create_fire()
    return f"Strength potion brewed with {earth} and {fire}"


def invisibility_potion() -> str:
    water = alchemy.create_water()
    air = alchemy.elements.create_air()
    return f"Invisibility potion brewed with {air} and {water}"
