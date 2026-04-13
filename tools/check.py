
import requests
import os
from security.iontoken import get_token
from dotenv import load_dotenv
import sys

load_dotenv()


def get_script_id(script_name):
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }

    url = f"{os.environ.get('ION_TENANT_URL')}/IONSERVICES"

    r = requests.get(
        f"{url}/scriptingservice/model/v1/scripts?name={script_name}",
        headers=headers,
        timeout=30
    )

    if r.status_code == 404:
        print("First call returned 404")
    elif r.status_code == 200:
        data = r.json()
        if data:
            print(f"""Script {script_name} found.
Approved Version: {data[0].get('lastApprovedVersionNumber')}""")
        else:
            print(f"Script {script_name} not found in first call.")
    else:
        print(f"First call returned status {r.status_code}")

    r1 = requests.get(
        f"{url}/scriptingservice/model/v1/scripts/{script_name}",
        headers=headers,
        timeout=30
    )

    if r1.status_code == 404:
        return False

    if r1.status_code == 200:
        print(f"""Latest Version: {r1.json().get('versionNumber')}
Latest Version Status: {r1.json().get('status')}
Last Updated By: {r1.json().get('lastUpdatedBy')}
Last Updated On: {r1.json().get('lastUpdatedOn')}""")
        return True

    print(f"Script {script_name} not found.")
    return False

get_script_id(script_name=sys.argv[1])

