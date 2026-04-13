import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from security.iontoken import get_token

load_dotenv()

# values from your .ionapi
# ci = "..."
# cs = "..."
# pu = "https://mingle-sso.inforcloudsuite.com:443"
# ot = "/YOUR_TOKEN_PATH"   # from ionapi
# saak = "..."
# sask = "..."
# iu = "https://ionapi.inforcloudsuite.com"
# ti = "YOUR_TENANT"
flow_name = "Stitch"

token = get_token()

base_url = f"{os.environ.get('ION_TENANT_URL')}"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# 1) list
list_url = f"{base_url}/IONSERVICES/connect/model/v1/dataflows"
list_resp = requests.get(list_url, headers=headers, timeout=60)
list_resp.raise_for_status()
items = list_resp.json()

print("LIST COUNT:", len(items))
print(json.dumps(items[:3], indent=2) if isinstance(items, list) else json.dumps(items, indent=2)[:2000])

# 2) detail
detail_url = f"{base_url}/IONSERVICES/connect/model/v1/dataflows/{flow_name}"
detail_resp = requests.get(detail_url, headers=headers, timeout=60)
detail_resp.raise_for_status()
flow = detail_resp.json()

Path(f"{flow_name}.json").write_text(json.dumps(flow, indent=2), encoding="utf-8")
print(f"Saved {flow_name}.json")
print(json.dumps(flow, indent=2)[:4000])

