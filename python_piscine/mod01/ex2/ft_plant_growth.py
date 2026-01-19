class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age
    def ft_print(self):
        print(f"{self.name}: {self.height}cm {self.age} days old")
    def modif(self):
        self.height += 1
        self.age += 1
if __name__ == "__main__":
    lst = [
        Plant("Rose", 25, 2)
    ]
    days = 7
    count = lst[0].height
    for i in range(1, days + 1):
        print(f"=== Day {i} ===")
        for p in lst:
            p.ft_print()
            p.modif()
    count = lst[0].height - (count + 1)
    print(f"Growth this week: +{count}cm")
    