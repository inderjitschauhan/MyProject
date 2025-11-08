# main.py
import subprocess
import sys
import os

def install_requirements(requirements_file="requirements.txt"):
    try:
        import pkg_resources
    except ImportError:
        print("📦 Installing setuptools...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
        import pkg_resources

    # Ensure requirements.txt path is relative to this script
    requirements_file = os.path.abspath(requirements_file)

    if not os.path.exists(requirements_file):
        print(f"❌ requirements.txt not found at {requirements_file}")
        return

    with open(requirements_file, "r") as f:
        required = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for pkg in required:
        try:
            # Check if requirement is already satisfied (with version)
            pkg_resources.require(pkg)
            print(f"✅ {pkg} already satisfied.")
        except pkg_resources.DistributionNotFound:
            print(f"📦 Installing missing: {pkg} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        except pkg_resources.VersionConflict as e:
            print(f"⚠️ Version conflict for {pkg}: {e}. Reinstalling...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

if __name__ == "__main__":
    install_requirements()
