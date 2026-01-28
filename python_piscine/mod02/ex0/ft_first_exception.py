def check_tmp(str):
    try:
        val = int(str)
        if val > 40:
            print(f"Error: {val}°C is too hot for plants (max 40°C)\n")
        elif val < 0:
            print(f"Error: {val}°C is too cold for plants (min 0°C)\n")
        else:
            print(f"Temperature {val}°C is perfect for plants!\n")
    except:
        print(f"Error: '{str}' is not a valid number\n")

def test_temperature_input():
    tests = ["12", "abc", "100", "-100"]
    print("=== Garden Temperature Checker ===\n")
    for p in tests:
        print(f"Testing temperature: {p}")
        check_tmp(p)
    print("All tests completed - program didn't crash!")
if __name__ == "__main__":
    test_temperature_input()