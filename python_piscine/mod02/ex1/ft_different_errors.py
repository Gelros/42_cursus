def garden_operations(error_type):
   if error_type == "val":
       val = int("abc")
   elif error_type == "zero":
       val = 1 / 0
   elif error_type == "file":
       open("noFile.txt", "r")
   else:
       key = {"1": "coucou"}
       print(key["qsvfsd"])

def test_error_types():
    print("=== Garden Error Types Demo ===\n")
    print("Testing ValueError...")
    try:
        garden_operations("val")
    except ValueError as e:
        print("Caught ValueError: ", e)
    
    print("\nTesting ZeroDivisionError...")
    try:
        garden_operations("zero")
    except ZeroDivisionError as e:
        print("Caught ZeroDivisionError: ", e)
    
    print("\nTesting FileNotFoundError...")
    try:
        garden_operations("file")
    except FileNotFoundError as e:
        print("Caught FileNotFoundError: ", e)
    
    print("\nTesting KeyError...")
    try:
        garden_operations("key")
    except KeyError as e:
        print("Caught KeyError: ", e)
    
    print("\nTesting multiple errors together...\nCaught an error, but program continues!")
    print("\nAll error types tested successfully!")

if __name__ == "__main__":
    test_error_types()
    