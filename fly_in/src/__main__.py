from src.parser import parse_map


def main() -> None:
    path = "maps/hard/02_capacity_hell.txt"
    
    parsed = parse_map(path)
    print(parsed.connexions)


if __name__ == "__main__":
    main()