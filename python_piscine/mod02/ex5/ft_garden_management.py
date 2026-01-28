class GardenError(Exception):
    pass
class PlantError(GardenError):
    pass
class WaterError(GardenError):
    pass

class GardenManager:
    def __init__(self):
        self.plants = []
        self.water_tank = 100
    def add_plant(self, plant):
        try:
            if not plant["name"]:
                raise PlantError("Error adding plant: Plant name cannot be empty!")
            self.plants.append(plant)
            print(f"Added {plant["name"]} successfully")
        except PlantError as e:
            print(e)

    def watering(self):
        print("Opening watering system")
        try:
            if self.water_tank < 20:
                raise WaterError("Not enought water in tank")
            for p in self.plants:
                print(f"Watering {p["name"]} - success")  
        except WaterError as e:
            print(e)
        finally:
            print("Closing watering system (cleanup)")
    
    def check_plant_health(self):
        plants = self.plants
        for plant in plants:
            try:
                if plant["water"] < 1 or plant["water"] > 10:
                    limit = "too low (min 1)" if plant["water"] < 1 else "too high (max 10)"
                    raise PlantError(f"Error checking {plant["name"]}: Water level {plant["water"]} is {limit}")
                elif plant["sun"] < 2 or plant["sun"] > 12:
                    limit = "too low (min 2)" if plant["sun"] < 2 else "too high (max 12)"
                    raise PlantError(f"Error checking {plant["name"]}: sun level {plant["sun"]} is {limit}")
                else:
                    print(f"{plant["name"]}: healthy (water: {plant["water"]}, sun: {plant["sun"]})")
            except PlantError as e:
                print(e)
    
    def water_err(self):
        self.water_tank = 2
        try:
            if self.water_tank < 20:
                raise WaterError("Not enought water in tank")
        except WaterError as e:
            print("Caught GardenError: ", e)
        finally:
            print("System recovered and continuing...")
    
def test():
    manager = GardenManager()
    print("=== Garden Management System ===")
    print("\nAdding plants to garden...")
    
    manager.add_plant({"name": "rose", "water": 1, "sun": 9})
    manager.add_plant({"name": "cactus", "water": 10, "sun": 0})
    manager.add_plant({"name": "Arbre", "water": 5, "sun": 9})
    
    print("\nWatering plants...")
    manager.watering()
    
    print("\nChecking plant health...")
    manager.check_plant_health()
    
    print("\nTesting error recovery...")
    manager.water_err()

    print("\nGarden management system test complete!")

if __name__ == "__main__":
    test()
    