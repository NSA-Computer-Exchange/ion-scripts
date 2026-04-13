import os
import time
import subprocess
import json
from security.auth import authenticate

TOKEN_CACHE_FILE = ".ion_token_cache.json"


def get_token():
    # If cache exists and not expired, reuse it
    if os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE) as f:
            cached = json.load(f)

        if cached["expires_at"] > time.time():
            return cached["access_token"]

    # Otherwise get new token
    result = authenticate()
    token = result["access_token"]
    expires_at = time.time() + 7100

    with open(TOKEN_CACHE_FILE, "w") as f:
        json.dump({
            "access_token": token,
            "expires_at": expires_at
        }, f)

    return token
