def check_plant_health(plant_name, water_level, sunlight_hours):
    try:
        if not plant_name:
            raise ValueError("Plant name cannot be empty!")
        if water_level < 1 or water_level > 10:
            if water_level > 10:
                raise ValueError(f"Water level {water_level} is too high (max 10)")
            else:
                raise ValueError(f"Water level {water_level} is too low (min 1)")
        if sunlight_hours < 2 or sunlight_hours > 12:
            if sunlight_hours > 12:
                raise ValueError(f"Sunlight hours {sunlight_hours} is too high (max 12)")
            else:
                raise ValueError(f"Sunlight hours {sunlight_hours} is too low (min 2)")
        print("Plant 'tomato' is healthy!")
    except ValueError as e:
        print(f"Error: {e}")

def test_plant_checks():
    print("=== Garden Plant Health Checker ===")
    
    print("\nTesting good values...")
    check_plant_health("Carrot", 3, 10)
    
    print("\nTesting empty plant name...")
    check_plant_health("", 3, 10)
    
    print("\nTesting bad water level...")
    check_plant_health("Carrot", 0, 10)
    
    print("\nTesting bad sunlight hours...")
    check_plant_health("Carrot", 3, 0)
    
    print("\nAll error raising tests completed!")

if __name__ == "__main__":
    test_plant_checks()