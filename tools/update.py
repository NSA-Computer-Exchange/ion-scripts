import sys, json, os, requests
from security.iontoken import get_token
from dotenv import load_dotenv

load_dotenv()


def update_script(script):
    #script = sys.argv[1]
    base = f"scripts/{script}"

    print(">>> Loading script files")

    with open(f"{base}/script.py") as f:
        code = f.read()

    with open(f"{base}/model.json") as f:
        model = json.load(f)

    model["scriptCode"] = code

    print(">>> Making PUT to ION scriptingservice")

    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }

    url = f"{os.environ.get('ION_TENANT_URL')}/IONSERVICES/scriptingservice/model/v1/scripts/{script}"

    r = requests.put(url, headers=headers, json=model)

    print(">>> Response received")
    print(r.status_code, r.text)
    print("Updated:", script)

    #if __name__ == "__main__":
update_script(sys.argv[1])