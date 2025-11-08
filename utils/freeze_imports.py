import sys
import pkg_resources

# Get all modules currently imported
imported_modules = set([name.split('.')[0] for name in sys.modules.keys() if name])

# Get installed packages in the environment
installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

# Filter installed packages to only those that are imported
required_packages = {}
for module in imported_modules:
    if module.lower() in installed_packages:
        required_packages[module.lower()] = installed_packages[module.lower()]

# Write to UTF-8 requirements.txt
with open("requirements.txt", "w", encoding="utf-8") as f:
    for pkg, ver in sorted(required_packages.items()):
        f.write(f"{pkg}=={ver}\n")

print("✅ requirements.txt created with only imported modules.")
