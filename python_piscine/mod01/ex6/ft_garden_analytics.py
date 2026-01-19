class Plant:
    def __init__(self, name, height):
        self.name = name
        self.height = height
        self.growth = 0
        self.points = 0

    def grow(self, value):
        self.growth += value
        self.height += value

    def __str__(self):
        return f"- {self.name}: {self.height}cm"


class FloweringPlant(Plant):
    def __init__(self, name, height, color):
        self.color = color
        super().__init__(name, height)

    def __str__(self):
        return f"{super().__str__()}, {self.color} flowers (blooming)"


class PrizeFlower(FloweringPlant):
    def __init__(self, name, height, color, points):
        super().__init__(name, height, color)
        self.points = points

    def __str__(self):
        return f"{super().__str__()}, Prize points: {self.points}"


class GardenManager:
    all_managers = []

    class GardenStat:
        @staticmethod
        def ft_sum(value):
            total = 0
            for p in value:
                total += p
            return total

        @staticmethod
        def ft_len(lst):
            count = 0
            for p in lst:
                count += 1
            return count

        @staticmethod
        def total_score(plants_list):
            return GardenManager.GardenStat.ft_sum(
                p.height + p.points for p in plants_list
            )

    def __init__(self, name):
        self.name = name
        self.plants = []
        self.stats_helper = self.GardenStat()
        GardenManager.all_managers.append(self)

    def add_plant(self, plant):
        self.plants.append(plant)
        print(f"Added {plant.name} to {self.name}'s garden")

    def growing(self, value):
        if value < 0:
            print(f"\nLa valeur de croissance doit etre positive !")

        else:
            print(f"\n{self.name} is helping all plants grow...")
            for p in self.plants:
                p.grow(value)
                print(f"{p.name} grew {p.growth}cm")

    def individual_report(self):
        print(f"\n=== {self.name}'s Garden Report ===")
        print("Plants in garden:")
        for p in self.plants:
            print(p)
        print(
            f"\nPlants added: {GardenManager.GardenStat.ft_len(self.plants)}, ", end=""
        )
        print(
            f"Total growth: {GardenManager.GardenStat.ft_sum(p.growth for p in self.plants)}cm"
        )
        print(
            f"Plant types:  {GardenManager.type_verif(self.plants, Plant)} regular, {GardenManager.type_verif(self.plants, FloweringPlant)} flowering, {GardenManager.type_verif(self.plants, PrizeFlower)} prize flowers"
        )

    @staticmethod
    def type_verif(plants_list, target):
        count = 0
        for p in plants_list:
            if p.__class__ == target:
                count += 1
        return count

    @staticmethod
    def is_neg(all_managers):
        for p in all_managers:
            for m in p.plants:
                if m.height < 0:
                    print("\nHeight validation test: False")
                    return
        print("\nHeight validation test: True")

    @classmethod
    def create_garden_network(cls, value):
        m = cls.all_managers[0]
        m.growing(value)
        m.individual_report()
        print(
            f"\nGarden score - {m.name}: {GardenManager.GardenStat.total_score(m.plants)}",
            end="",
        )
        GardenManager.is_neg(cls.all_managers)
        for garden in cls.all_managers[1:]:
            print(
                f", {garden.name}: {cls.GardenStat.total_score(garden.plants)}", end=""
            )
        print(f"Total gardens managed: {cls.GardenStat.ft_len(cls.all_managers)}")

if __name__ == "__main__":
    alice = GardenManager("Alice")
    bob = GardenManager("Bob")

    print("=== Garden Management System Demo ===\n")
    alice.add_plant(FloweringPlant("Rose", 32, "red"))
    alice.add_plant(PrizeFlower("Orchidée", 34, "white", 10))
    bob.add_plant(Plant("Pacrette", 3))
    GardenManager.create_garden_network(2)
