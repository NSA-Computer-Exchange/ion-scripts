import sys, os, requests
from dotenv import load_dotenv
from security.iontoken import get_token

load_dotenv()

def approve_script(script):
    script = sys.argv[1]

    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {get_token()}"
    }

    url = f"{os.environ.get('ION_TENANT_URL')}/IONSERVICES/scriptingservice/model/v1/scripts/{script}/approve"

    r = requests.put(url, headers=headers)
    r.raise_for_status()
    return print("Approved:", script)

if __name__ == "__main__":
    approve_script(sys.argv[1])