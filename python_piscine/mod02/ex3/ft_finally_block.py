def  water_plants(plant_list):
    try:
        err = False
        for p in plant_list:
            plant = "Watering "
            plant += p
            print(plant)
    except:
        print(f"Error: Cannot water {p} - invalid plant!")
        err = True
    finally:
        print("Closing watering system (cleanup)")
        if err:
            print("\nCleanup always happens, even with errors!")
        else:
            print("Watering completed successfully!")

def test_watering_system():
    without_err = ["Tomato", "Cactus", "Lettuce"]
    with_err = ["Tomato", None]
    print("=== Garden Watering System ===")
    print("\nTesting normal watering...")
    water_plants(without_err)
    print("\nTesting with error...")
    water_plants(with_err)

if __name__ == "__main__":
    test_watering_system()