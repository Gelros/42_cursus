import time
from functools import wraps
import random


def spell_timer(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"Casting {func.__name__}")
        res = func(*args, **kwargs)
        end = time.time()
        total_time = round(end - start, 3)
        print(f"Spell completede in {total_time}")
        return res
    return wrapper


def power_validator(min_power: int) -> callable:
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if func.__name__ == "cast_spell":
                power = args[2]
            else:
                power = args[0]
            if power <= min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)
        return wrapper
    return deco


def retry_spell(max_attempts: int) -> callable:
    def retry(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    if random.random() < 0.7:
                        raise Exception()
                    return func(*args, **kwargs)
                except Exception:
                    print(
                        "Spell failed, retrying..."
                        f"(attempt {attempt}/{max_attempts})")
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return retry


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3 or not name.replace(" ", "").isalpha():
            return False
        return True

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main():
    @spell_timer
    def fireball():
        return "Fireball cast!"
    print("\nTesting spell_timer...")
    print(fireball())

    @power_validator(10)
    def spell_power(power, name):
        return f"Spell power: {power}, name: {name}"
    print("\nTesting power_validator...")
    print(spell_power(40, "fireball"))

    max_attempt = 5

    @retry_spell(max_attempt)
    def ice_pic(power: int, target):
        return f"Ice pic hit {target}"
    print("\nTesting retry_spell...")
    print(ice_pic("f", "dragon"))

    print("\nTesting MageGuild...")
    mage = MageGuild()
    print(mage.validate_mage_name("Merlin"))
    print(mage.validate_mage_name("123"))
    print(mage.cast_spell("fireball", 15))
    print(mage.cast_spell("fireball", 1))


if __name__ == "__main__":
    main()
