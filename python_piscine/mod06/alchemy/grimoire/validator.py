def validate_ingredients(ingredients: str) -> str:
    elem = ["fire", "air", "water", "earth"]
    is_valid = any(i in ingredients.lower() for i in elem)
    if is_valid:
        return f"[{ingredients}] - VALID"
    return f"[{ingredients}] - INVALID"
