# utils/api_client.py

import json
import urllib.parse
import requests
from pathlib import Path
from typing import Optional, Dict

def load_cookies_from_storage(path: str = "storage/auth.json") -> Dict[str, str]:
    """
    Reads Playwright's storage_state JSON and returns a simple cookie dict
    suitable for requests.
    """
    with open(path, encoding="utf-8") as f:
        state = json.load(f)
    return {c["name"]: c["value"] for c in state.get("cookies", [])}


# Load the captured template once
_tpl_path = Path("data/api_template.json")
with _tpl_path.open(encoding="utf-8") as f:
    _tpl = json.load(f)


def send_prompt_direct(
    message: str,
    recaptcha_token: str = "TEST_TOKEN",
    cookies: Optional[Dict[str, str]] = None
) -> str:
    # build form data by replacing placeholders
    form_fields = {}
    for key, val in _tpl["form_template"].items():
        if val == "{message}":
            form_fields[key] = message
        elif val == "{recaptcha_token}":
            form_fields[key] = recaptcha_token
        else:
            form_fields[key] = val

    # URL-encode the form data
    data = urllib.parse.urlencode(form_fields, doseq=True)

    # make the request
    resp = requests.post(
        _tpl["url"],
        data=data,
        headers=_tpl["headers"],
        cookies=cookies or {}
    )
    resp.raise_for_status()
    print(f"=======api response========{resp.text}")
    payload = resp.json()

    # extract the last user->bot message
    msgs = payload.get("Messages") or []
    if isinstance(msgs, list) and msgs:
        return msgs[-1].get("content", "").strip()

    # fallback
    return payload.get("reply", "").strip()
