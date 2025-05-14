import os

# ─── Language & Base URL ────────────────────────────────────────────────
# Change this to "ar" to run tests in Arabic

LANG = "en"
BASE_URLS = {
    "en": "https://ask.u.ae/en/",
    "ar": "https://ask.u.ae/ar/"
}

# Supported values
if LANG not in ("en", "ar"):
    raise ValueError(f"Unsupported LANG='{LANG}'; must be 'en' or 'ar'.")

BASE_URL = BASE_URLS[LANG]


# ─── Timeout Settings (milliseconds) ────────────────────────────────────

DEFAULT_TIMEOUT = 10000   # e.g. page.goto, navigation
SHORT_TIMEOUT   =  5000   # quick visibility checks
LONG_TIMEOUT    = 30000   # slow ops (AI streaming)


# ─── Playwright Launch Settings ────────────────────────────────────────

# Defaults to headful (visible browser); set HEADLESS=true to override
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"


# ─── Reporting & Artifacts ──────────────────────────────────────────────

ALLURE_RESULTS_DIR = os.getenv("ALLURE_DIR", "report/allure-results")
TRACE_RESULTS_DIR  = os.getenv("TRACE_DIR",  "report/traces")


# ─── Session Persistence ────────────────────────────────────────────────

# storage_state.json for re-using login/CAPTCHA
STORAGE_STATE_PATH = os.getenv("STORAGE_STATE_PATH", "storage/auth.json")
