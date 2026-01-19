def ft_garden_intro(name: str, height: int, age: int) -> None:
    print("=== Welcome to My Garden ===")
    print(f"Plant: {name}")
    print(f"Height: {height}cm")
    print(f"Age: {age} days\n")
    print("=== End of Program ===")
if __name__ == "__main__":
    plant_name = "Rose"
    height = 25
    age = 1
    ft_garden_intro(plant_name, height, age)