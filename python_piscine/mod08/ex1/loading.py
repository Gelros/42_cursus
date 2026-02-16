import importlib.util
import numpy as np
import matplotlib.pyplot as plt


def check_dependency(package_name: str) -> tuple[bool, str]:
    """Check if a package is installed and return its version."""
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            return False, "Not installed"
        module = __import__(package_name)
        version = getattr(module, "__version__", "unknown")
        return True, version
    except Exception:
        return False, "Not installed"


def all_check() -> bool:
    """Check all required dependencies and display their status."""
    packages = ["pandas", "numpy", "matplotlib", "requests"]
    all_ok = True

    for package in packages:
        ok, ver = check_dependency(package)
        if ok:
            print(f"  [OK] {package} ({ver})")
        else:
            print(f"  [MISSING] {package} - run: pip install {package}")
            all_ok = False
    return all_ok


def analyze_matrix_data() -> None:
    """Analyze simulated Matrix data and generate visualization."""
    print("\nAnalyzing Matrix data...")

    data = np.random.randn(1000)
    print("Processing 1000 data points...")

    print("Generating visualization...")
    plt.plot(data, color="green", alpha=0.7)
    plt.title("Matrix Data Analysis")
    plt.savefig("matrix_analysis.png")
    plt.close()

    print("\nAnalysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    print("\nLOADING STATUS: Loading programs...\n")
    if all_check():
        analyze_matrix_data()
    else:
        print("\nPlease install missing dependencies first.")
