def record_spell(spell_name: str, ingredients: str) -> str:
    from .validator import validate_ingredients

    validate = validate_ingredients(ingredients)

    if "VALID" in validate:
        return f"Spell recorded: [{spell_name}] ([{validate}])"
    else:
        return f"Spell rejected: [{spell_name}] ([{validate}])"
