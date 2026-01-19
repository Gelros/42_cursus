class SecurePlant:
    def __init__(self, name, height, age):
        self.__name = name
        print(f"Plant created: {name}")
        self.set_height(height)
        self.set_age(age)

    def set_height(self, height):
        if height >= 0:
            self.__height = height
            print(f"Height updated: {height}cm [OK]")
        else:
            print(f"\nInvalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")

    def set_age(self, age):
        if age >= 0:
            self.__age = age
            print(f"Age updated: {age} days [OK]")
            
        else:
            print(f"\nInvalid operation attempted: age {age} days [REJECTED]")
            print("Security: Negative age rejected")

    def get_height(self) -> int:
        return self.__height

    def get_age(self) -> int:
        return self.__age

    def get_name(self) -> str:
        return self.__name

if __name__ == "__main__":
    print("=== Garden Security System ===")
    
    plant = SecurePlant("Rose", 20, 10)

    plant.set_height(25)
    plant.set_age(30)

    plant.set_age(5)

    print(f"Current plant: {plant.get_name()} ({plant.get_height()}cm, {plant.get_age()} days)")
