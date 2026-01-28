class GardenError(Exception):
    pass

class PlantError(GardenError):
    pass

class WaterError(GardenError):
    pass

def plant_err(is_wilting):
    if is_wilting:
        raise PlantError("The tomato is wilting !")

def water_err(is_water):
    if is_water:
        raise WaterError("Not enough water in the tank!")


def error():
    tab = []
    
    print("=== Custom Garden Errors Demo ===")
    print("\nTesting PlantError...")
    try:
        tab.append({"f":plant_err, "arg": True})
        plant_err(True)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
    
    print("\nTesting WaterError...")
    try:
        tab.append({"f":water_err, "arg": True})
        water_err(True)
    except WaterError as e:
        print(f"Caught WaterError: {e}")
    
    print("\nTesting catching all garden errors...")
    for p in tab:
        try:
            p["f"](p["arg"])
        except GardenError as e:
            print(f"Caught a garden error: {e}")
    print("\nAll custom error types work correctly!")

if __name__ == "__main__":
    error()
