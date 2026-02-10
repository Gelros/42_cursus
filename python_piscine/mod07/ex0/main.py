from CreatureCard import CreatureCard


def main():
    obj = CreatureCard("Dino", 10, "rare", 10, 5)
    print(obj.get_card_info())


if __name__ == "__main__":
    main()
