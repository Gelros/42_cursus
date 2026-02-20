def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    n_lst = list(sorted(artifacts, key=lambda obj: obj["power"], reverse=True))
    return n_lst


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    filted = list(filter(lambda power: power["power"] >= min_power, mages))
    return filted


def spell_transformer(spells: list[str]) -> list[str]:
    new_lst = list(map(lambda spell: f"* {spell} *", spells))
    return new_lst


def mage_stats(mages: list[dict]) -> dict:
    most_powerful = max(mages, key=lambda power: power["power"])
    least_powerful = min(mages, key=lambda power: power["power"])
    sum_power = sum(power["power"] for power in mages)
    avg = sum_power / len(mages)

    return {
        "max_power": most_powerful["power"],
        "min_power": least_powerful["power"],
        "avg_power": avg
    }


def main():
    mages = [
        {"name": "Ricard", "power": 12, "element": "fire"},
        {"name": "Merlin", "power": 8, "element": "water"},
        {"name": "Robert", "power": 10, "element": "earth"},
    ]

    artifacts = [
        {"name": "Fire Staff", "power": 40, "type": "offensive"},
        {"name": "Ice Staff", "power": 39, "type": "offensive"},
        {"name": "Crystal Orb", "power": 12, "type": "defensive"}
    ]

    print("Testing mages stats:")
    print(mage_stats(mages))

    spells = ["fireball", "heal", "shield"]
    print("\nTesting spell transformer:")
    print(*spell_transformer(spells))

    print("\nTesting power filter:")
    for obj in power_filter(mages, 10):
        print(obj)

    print("\nTesting artifact sorter...")
    len_art = len(artifact_sorter(artifacts)) - 1
    for i, obj in enumerate(artifact_sorter(artifacts)):
        if i == len_art:
            print(f"{obj["name"]} ({obj["power"]} power)")
        else:
            print(f"{obj["name"]} ({obj["power"]} power), ", end="")


if __name__ == "__main__":
    main()
