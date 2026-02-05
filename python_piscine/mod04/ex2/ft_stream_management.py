import sys


def main():
    print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n")

    sys.stdout.write("Input Stream active. Enter archivist ID: ")
    input_id = input()

    sys.stdout.write("Input Stream active. Enter status report: ")
    input_report = input()

    print(f"\n[STANDARD] Archive status from {input_id}: {input_report}")
    print("[ALERT] System diagnostic: Communication channels verified", file=sys.stderr)
    print("[STANDARD] Data transmission complete\n")

    print("Three-channel communication test successful.")


if __name__ == "__main__":
    main()