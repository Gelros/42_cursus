class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def ft_print(self):
        print(f"{self.name}: {self.height}cm, {self.age} days old")


if __name__ == "__main__":
    lst = [
        Plant("Rose", 21, 34),
        Plant("Cactus", 12, 14),
        Plant("Mandragore", 6, 4)
    ]
    print("=== Garden Plant Registry ===")
    for i in lst:
        i.ft_print()
