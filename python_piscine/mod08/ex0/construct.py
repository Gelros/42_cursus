import sys
import site
import os

if __name__ == "__main__":
    env = sys.prefix != sys.base_prefix
    if not env:
        print(
            "\nMATRIX STATUS: You're still plugged in\n\n"

            f"Current Python: {sys.executable}\n"
            "Virtual Environment: None detected\n\n"

            "WARNING: You're in the global environment!\n"
            "The machines can see everything you install.\n\n"

            "To enter the construct, run:\n"
            "python -m venv matrix_env\n"
            "source matrix_env/bin/activate # On Unix\n"
            "matrix_env\n"
            "Scripts\n"
            "activate # On Windows\n\n"

            "Then run this program again."
        )
    else:
        print(
            "\nMATRIX STATUS: Welcome to the construct\n\n"

            f"Current Python: {sys.executable}\n"
            f"Virtual Environment: {os.path.basename(sys.prefix)}\n"
            f"Environment Path: {sys.prefix}\n\n"

            "SUCCESS: You're in an isolated environment!\n"
            "Safe to install packages without affecting the global system.\n\n"

            "Package installation path:\n"
            f"{site.getsitepackages()[0]}"
        )
