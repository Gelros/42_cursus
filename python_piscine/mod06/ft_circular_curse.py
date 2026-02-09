from alchemy.grimoire import validate_ingredients, record_spell


def main():

    print("\n=== Circular Curse Breaking ===\n")

    print("Testing ingredient validation:")
    test_valid = validate_ingredients("fire air")
    test_invalid = validate_ingredients("dragon scales")
    print(f'validate_ingredients("fire air"): {test_valid}')
    print(f'validate_ingredients("dragon scales"): {test_invalid}')

    print("\nTesting spell recording with validation:")
    valid_record = record_spell("Fireball", "fire air")
    invalid_record = record_spell("Dark Magic", "shadow")
    print(f'record_spell("Fireball", "fire air"): {valid_record}')
    print(f'record_spell("Dark Magic", "shadow"): {invalid_record}')

    print("\nTesting late import technique:")
    test_late = record_spell("Lightning", "air")
    print(f'record_spell("Lightning", "air"): {test_late}')

    print("\nCircular dependency curse avoided using late imports!")
    print("All spells processed safely!")


if __name__ == "__main__":
    main()
