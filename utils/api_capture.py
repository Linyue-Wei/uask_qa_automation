# utils/api_capture.py

import json
import urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT = Path("data/api_template.json")

def main():
    captured = {}

    def on_request(request):
        # only capture the AskStream POST
        if request.method == "POST" and "AskStream" in request.url and not captured:
            captured["url"] = request.url

            # pare down to the headers you'll need  
            headers = {}
            for k, v in request.headers.items():
                kl = k.lower()
                if kl in (
                    "accept",
                    "content-type",
                    "x-requested-with",
                    "origin",
                    "referer",
                    "user-agent",
                ):
                    headers[k] = v
            captured["headers"] = headers

            # parse form‐encoded body
            raw = request.post_data
            parsed = urllib.parse.parse_qs(raw, keep_blank_values=True)
            template = {}
            for key, vals in parsed.items():
                # Messages[0][content] → placeholder
                if key.endswith("[content]"):
                    template[key] = "{message}"
                # RecaptchaToken → placeholder
                elif key == "RecaptchaToken":
                    template[key] = "{recaptcha_token}"
                else:
                    template[key] = vals[0]
            captured["form_template"] = template

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        # use your saved auth so we don’t re-trigger CAPTCHA
        ctx     = browser.new_context(storage_state="storage/auth.json")
        ctx.on("request", on_request)

        page = ctx.new_page()
        page.goto("https://ask.u.ae/en/", timeout=60000)
        # page.click("role=button[name='Accept and continue']")
        # send a dummy message to fire the request
        page.fill(".expando-textarea", "TemplateCapture")
        page.keyboard.press("Enter")

        # give it a moment to fire
        page.wait_for_timeout(3000)
        browser.close()

    # ensure output directory exists
    OUTPUT.parent.mkdir(exist_ok=True)
    # write out the captured template
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(captured, f, indent=2, ensure_ascii=False)

    print(f"✅ Wrote API template to {OUTPUT!r}")

if __name__ == "__main__":
    main()
