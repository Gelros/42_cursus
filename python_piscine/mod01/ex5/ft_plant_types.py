class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def get_info(self):
        return self.__class__.__name__

    def ft_print(self):
        print(f"\n{self.name} ({self.get_info()}): ", end="")
        print(f"{self.height}cm, {self.age} days", end="")


class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color

    def ft_print(self):
        super().ft_print()
        print(f", {self.color} color")
        print(f"{self.name} is blooming beautifully!")


class Tree(Plant):
    def __init__(self, name, height, age, diameter):
        super().__init__(name, height, age)
        self.diameter = diameter

    def ft_print(self):
        super().ft_print()
        print(f", {self.diameter}cm diameter")
        print(f"{self.name} provides 78 square meters of shade")


class Vegetable(Plant):
    def __init__(self, name, height, age, season):
        super().__init__(name, height, age)
        self.season = season

    def ft_print(self):
        super().ft_print()
        print(f", {self.season} harvest")
        print(f"{self.name} is rich in vitamin C")


if __name__ == "__main__":
    garden = [
        Flower("Rose", 25, 45, "red"),
        Tree("Oak", 800, 1567, 55),
        Vegetable("Tomato", 18, 15, "summer"),
    ]
    print("=== Garden Plant Types ===")
    for i in garden:
        i.ft_print()
