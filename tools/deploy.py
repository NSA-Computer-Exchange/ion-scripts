import sys, json, os, requests
from tools.check import get_script_id
from tools.update import update_script
from security.iontoken import get_token
from tools.approve import approve_script
from dotenv import load_dotenv

load_dotenv()

script = sys.argv[1]
base = f"scripts/{script}"

print(">>> Loading script files")

with open(f"{base}/script.py") as f:
    code = f.read()

with open(f"{base}/model.json") as f:
    model = json.load(f)

model["scriptCode"] = code

print(">>> Making POST to ION scriptingservice")

headers = {
    "Authorization": f"Bearer {get_token()}",
    "Content-Type": "application/json",
    "Accept": "*/*"
}

url = f"{os.environ.get('ION_TENANT_URL')}/IONSERVICES/scriptingservice/model/v1/scripts"; print(url)


# Check if script already exists
if get_script_id(script):
    print(f"Script {script} already exists. Will try to update instead of create.")
    #update_script(script)
    if update_script(script):
        print(f"Script {script} updated successfully.")
        approve_script(script)
        print(f"Script {script} approved successfully.")
else:
    # Script does not exist, create it
    r = requests.post(url, headers=headers, json=model)
    
    print(">>> PAYLOAD BEING SENT")
    print(json.dumps(model, indent=2))

    print(">>> Response received, creating new script")
    print(r.status_code, r.text)
    if r.status_code == 201:

        print(f"Script {script} created successfully.")
        approve_script(script)
        print(f"Script {script} approved successfully.")
    else:
        print(f"Failed to create script {script}.")
