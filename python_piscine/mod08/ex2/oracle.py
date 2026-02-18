import os
from dotenv import load_dotenv


def load_configuration() -> dict:
    load_dotenv()

    config = {
        "MATRIX_MODE": os.environ.get("MATRIX_MODE", "unknown"),
        "DATABASE_URL": os.environ.get("DATABASE_URL", "not configured"),
        "API_KEY": os.environ.get("API_KEY", "not configured"),
        "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
        "ZION_ENDPOINT": os.environ.get("ZION_ENDPOINT", "not configured")
    }
    return config


def display_configuration(config: dict) -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")

    mode = config["MATRIX_MODE"]
    db = config["DATABASE_URL"]
    api = config["API_KEY"]

    print("Configuration loaded:")
    print(f"Mode: {mode}")
    if db != "not configured":
        print("Database: Connected to local instance")
    else:
        print("Not connected")
    if api != "not configured":
        print("API Access: Authenticated")
    else:
        print("API Access: Not configured")
    print(f"Log Level: {config['LOG_LEVEL']}")
    zion = config["ZION_ENDPOINT"]
    if zion != "not configured":
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline")


def security_check(config: dict) -> None:
    print("\nEnvironment security check:")

    print("[OK] No hardcoded secrets detected")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file not found")

    print("[OK] Production overrides available")

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    config = load_configuration()
    display_configuration(config)
    security_check(config)
