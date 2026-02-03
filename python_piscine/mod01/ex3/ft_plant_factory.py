class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def ft_print(self):
        print(f"Created: {self.name.capitalize()} ", end="")
        print(f"({self.height}cm, {self.age} days)")


if __name__ == "__main__":
    generate_name = ["Rose", "Eucalyptus", "Cactus", "Paquerette"]
    garden = []
    n = 0
    for i in generate_name:
        n += 1
    print("=== Plant Factory Output ===")
    for i in range(0, n):
        name = generate_name[i]
        height = (i + 32) * i + 32
        age = i * i + 2
        garden.append(Plant(name, height, age))
    for i in garden:
        i.ft_print()
    print(f"\nTotal plants created: {n}")
