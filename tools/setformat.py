import sys
import json
from pathlib import Path

VALID_FORMATS = ["Text", "JSON", "XML", "CSV", "Base64"]

def usage():
    print("Usage:")
    print("  python3 -m tools.setformat <ScriptName> --input FORMAT")
    print("  python3 -m tools.setformat <ScriptName> --output FORMAT")
    sys.exit(1)

def main():
    if len(sys.argv) < 4:
        usage()

    script = sys.argv[1]
    option = sys.argv[2]
    value = sys.argv[3]

    if value not in VALID_FORMATS:
        print(f"Invalid format. Must be one of: {', '.join(VALID_FORMATS)}")
        sys.exit(1)

    base_path = Path("scripts") / script
    meta_path = base_path / "meta.json"

    if not meta_path.exists():
        print(f"No meta.json found for {script}")
        sys.exit(1)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    if option == "--input":
        meta["input_format"] = value
    elif option == "--output":
        meta["output_format"] = value
    else:
        usage()

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Updated {script} meta.json → {option.replace('--','')} = {value}")

if __name__ == "__main__":
    main()