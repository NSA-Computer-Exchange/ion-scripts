import sys
import json
import os
import requests
from pathlib import Path
from security.iontoken import get_token
from dotenv import load_dotenv
import base64

load_dotenv()

if len(sys.argv) < 2:
    print("Usage: python3 -m tools.run <ScriptName>")
    sys.exit(1)

script = sys.argv[1]
base_path = Path(f"scripts/{script}")

# ---------------------------------------------------
# Load raw input (format-agnostic)
# ---------------------------------------------------
input_path = base_path / "test-input.txt"

if not input_path.exists():
    raise RuntimeError(f"Missing test-input.txt in {base_path}")

with open(input_path, "r", encoding="utf-8") as f:
    test_input = f.read()

payload = {
    "data_in": test_input
}

# ---------------------------------------------------
# Load meta data (optional, for format hints)
# ---------------------------------------------------
meta_path = base_path / "meta.json"

meta = {}
if meta_path.exists():
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

output_format = meta.get("output_format")

# ---------------------------------------------------
# Headers
# ---------------------------------------------------
token = get_token()
if not token:
    raise RuntimeError("get_token() returned empty token")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "*/*"
}

url = f"{os.environ.get('ION_TENANT_URL')}/IONSERVICES/scriptingservice/engine/v1/scripts/{script}/execute"

print(f">>> Executing script: {script}")
print(f">>> Endpoint: {url}")

# ---------------------------------------------------
# Execute
# ---------------------------------------------------
r = requests.post(url, headers=headers, json=payload, timeout=30)

if not r.ok:
    print("STATUS:", r.status_code)
    print("BODY:", r.text)
    sys.exit(1)

data = r.json()

# ---------------------------------------------------
# Validate output
# ---------------------------------------------------
if "data_out" not in data:
    raise RuntimeError(f"No data_out in response: {data}")

output = data["data_out"]

if output is None or (isinstance(output, str) and not output.strip()):
    raise RuntimeError("Script returned empty output")



# ---------------------------------------------------
# Save output intelligently
# ---------------------------------------------------
os.makedirs("tests", exist_ok=True)

if output_format == "JSON":
    with open("tests/output.json", "w", encoding="utf-8") as f:
        json.dump(json.loads(output), f, indent=2)
elif output_format == "XML":
    with open("tests/output.xml", "w", encoding="utf-8") as f:
        f.write(output)
elif output_format == "CSV":
    with open("tests/output.csv", "w", encoding="utf-8") as f:
        f.write(output)
elif output_format == "Base64":
    with open("tests/output.bin", "wb") as f:
        f.write(base64.b64decode(output))
else:
    # fallback to text
    with open("tests/output.txt", "w", encoding="utf-8") as f:
        f.write(output)

# ---------------------------------------------------
# Console preview
# ---------------------------------------------------
print("\n=== OUTPUT PREVIEW (first 500 chars) ===\n")

if isinstance(output, str):
    print(output[:500])
else:
    print(str(output)[:500])

print(f"\n>>> Saved as tests/output.{output_format if output_format != 'Base64' else 'bin'}")