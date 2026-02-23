from functools import reduce, partial, lru_cache, singledispatch
import operator


def spell_reducer(spells: list[int], operation: str) -> int:
    """reduce renvoie un seul nombre selon une instruction"""
    operations = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min
    }
    return reduce(operations[operation], spells)


def partial_enchanter(base_enchantment: callable) -> dict[str, callable]:
    """Partial permet de pre-remplir les parametres dans l'ordre"""
    fire_enchant = partial(base_enchantment, 50, "fire")
    ice_enchant = partial(base_enchantment, 50, "ice")
    lightning_enchant = partial(base_enchantment, 50, "lightning")

    return {
        "fire_enchant": fire_enchant,
        "ice_enchant": ice_enchant,
        "lightning_enchant": lightning_enchant
    }


@lru_cache
def memoized_fibonacci(n: int) -> int:
    """lru_cache mémorise les résultats déjà calculés"""
    if n <= 1:
        return n
    return memoized_fibonacci(n-1) + memoized_fibonacci(n-2)


def spell_dispatcher() -> callable:
    """
    singledispatch permet d'avoir une fonction qui se comporte
    différemment selon le type de l'argument
    """
    @singledispatch
    def cast_spell(arg):
        return "Unknown spell type"

    @cast_spell.register(int)
    def _(arg):
        return f"Damage spell: {arg} damage"

    @cast_spell.register(str)
    def _(arg):
        return f"Enchantment: {arg}"

    @cast_spell.register(list)
    def _(arg):
        return f"Multi-cast: {arg}"

    return cast_spell


def main():
    print("\nTesting spell reducer...")
    nombres = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(nombres, 'add')}")
    print(f"Mul: {spell_reducer(nombres, 'multiply')}")
    print(f"Max: {spell_reducer(nombres, 'max')}")

    def enchant(power, element, target):
        return f"{element} enchantment of {power} on {target}"
    print("\nTest partial...")
    print(partial_enchanter(enchant)["fire_enchant"]("sword"))

    print("\nTesting memoized fibonacci...")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")

    print("\nTest spell dispatch...")
    res = spell_dispatcher()
    print(res("fire"))


if __name__ == "__main__":
    main()
