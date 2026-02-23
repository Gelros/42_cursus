def spell_combiner(spell1: callable, spell2: callable) -> callable:
    def combined(target):
        res1 = spell1(target)
        res2 = spell2(target)
        return (res1, res2)
    return combined


def power_amplifier(base_spell: callable, multiplier: int) -> callable:
    def ampli(target):
        res = base_spell(target)
        return res * multiplier
    return ampli


def conditional_caster(condition: callable, spell: callable) -> callable:
    def caster(target):
        res = spell(target)
        if condition(target):
            return res
        return "Spell fizzled"
    return caster


def spell_sequence(spells: list[callable]) -> callable:
    def spells_result(target):
        return list(spell(target) for spell in spells)
    return spells_result


def fireball(target):
    return f"Fireball hit {target}"


def heal(target):
    return f"Heal {target}"


def ampli(target):
    return 10


def main():
    print("\nTesting spell combiner...")
    comb = spell_combiner(fireball, heal)
    print(f"Combined spell result: {comb("Dragon")}")

    print("\nTesting power amplifier...")
    mega_spell = power_amplifier(ampli, 3)
    print(f"Original: {ampli("dragon")}, Amplified: {mega_spell("dragon")}")


if __name__ == "__main__":
    main()
