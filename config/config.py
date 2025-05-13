import os

# Default language for the test run ("en" or "ar")
LANG = os.getenv("UASK_LANG", "en").lower()

# Base URLs per language
_URLS = {"en": "https://ask.u.ae/en/", "ar": "https://ask.u.ae/ar/"}


def get_base_url() -> str:
    """
    Return the base URL based on the configured language.
    Raises if the language is unsupported.
    """
    if LANG not in _URLS:
        raise ValueError(f"Unsupported language: {LANG}")
    return _URLS[LANG]


# Timeout settings (in milliseconds)
DEFAULT_TIMEOUT = 10000
SHORT_TIMEOUT = 5000
LONG_TIMEOUT = 30000

# Playwright launch settings
# Defaults to headful (visible browser); set HEADLESS=true to override
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# Allure results directory (for pytest --alluredir)
ALLURE_RESULTS_DIR = os.getenv("ALLURE_DIR", "report/allure-results")
TRACE_RESULTS_DIR = os.getenv("TRACE_DIR", "report/traces")

# Path to the persisted storageState for CAPTCHA/session reuse
STORAGE_STATE_PATH = os.getenv("STORAGE_STATE_PATH", "storage/auth.json")
