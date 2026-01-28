import sys

def argv() -> None:
    argv = sys.argv[1:]
    len_arg = len(sys.argv) - 1
    print("=== Command Quest ===")
    if len_arg == 0:
        print("No arguments provided!")
    print(f"Program name: {sys.argv[0]}")
    if len_arg > 0:
        print("Arguemnts received:", len_arg)
        count = 0
        for arg in argv:
            count += 1
            print(f"Argument {count}: {arg}")
    print(f"Total arguments:", len(sys.argv))

if __name__ == "__main__":
    argv()