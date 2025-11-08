import sys

input_file = "requirements.txt"
output_file = "requirements.txt"

try:
    # Read raw bytes
    with open(input_file, "rb") as f:
        raw = f.read()

    # Detect encoding
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        # UTF-16 BOM
        content = raw.decode('utf-16')
    elif raw.startswith(b'\xef\xbb\xbf'):
        # UTF-8 BOM
        content = raw.decode('utf-8-sig')
    else:
        # Plain UTF-8
        content = raw.decode('utf-8')

    # Write back as UTF-8 without BOM
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ requirements.txt converted to UTF-8 without BOM")

except Exception as e:
    print(f"❌ Error converting requirements.txt: {e}")
    sys.exit(1)
