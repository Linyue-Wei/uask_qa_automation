import os
from playwright.sync_api import sync_playwright
from config.config import STORAGE_STATE_PATH, BASE_URL

USER_DATA_DIR = os.path.dirname(STORAGE_STATE_PATH) or "storage/session"


def main():
    os.makedirs(os.path.dirname(STORAGE_STATE_PATH), exist_ok=True)

    with sync_playwright() as pw:
        context = pw.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            timezone_id="Asia/Dubai"
        )
        page = context.new_page()
        page.goto(BASE_URL)

        print("\nPlease solve any CAPTCHA manually in the opened browser.")
        input("Once complete, press ENTER to save session and exit...\n")

        context.storage_state(path=STORAGE_STATE_PATH)
        print(f"Session state saved to: {STORAGE_STATE_PATH}")

        context.close()


if __name__ == "__main__":
    main()
