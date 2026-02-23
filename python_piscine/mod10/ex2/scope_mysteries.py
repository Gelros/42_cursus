def mage_counter() -> callable:
    counting = 0

    def count():
        nonlocal counting
        counting += 1
        return counting
    return count


def spell_accumulator(initial_power: int) -> callable:
    def accumulate(power):
        nonlocal initial_power
        initial_power += power
        return initial_power
    return accumulate


def enchantment_factory(enchantment_type: str) -> callable:
    def enchant(name):
        return f"{enchantment_type} {name}"
    return enchant


def memory_vault() -> dict[str, callable]:
    storage = {}

    def store(key, value):
        storage[key] = value

    def recall(key):
        if key in storage:
            return storage[key]
        return "Memory not found"
    return {"store": store, "recall": recall}


def main():
    print("\nTesting mage counter...")
    count = mage_counter()
    for i in range(1, 4):
        print(f"Call {i}: {count()}")

    total_power = spell_accumulator(10)
    print(f"\nAvant: {total_power(0)}")
    print(f"Apres: {total_power(40)}")

    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    print(flaming("Sword"))

    vault = memory_vault()
    vault["store"]("sword", "excalibur")
    print()
    print(vault["recall"]("sword"))


if __name__ == "__main__":
    main()
