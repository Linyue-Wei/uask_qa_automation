# U-Ask QA Automation Framework

A Python-based end-to-end automated test framework for the U-Ask generative AI chatbot ([https://ask.u.ae](https://ask.u.ae)).

This framework covers:

* **UI Behavior**: Chat widget loading, message sending/receiving, layout, scrolling, accessibility
* **AI Response Validation**: Ensuring relevance, consistency, formatting, and absence of hallucinations
* **Security & Injection Handling**: Input sanitization and resistance to malicious prompts

---

## 🚀 Project Structure

```
uask_qa_automation/
├── config/                    # Environment & feature flags
│   └── config.py              # Base URLs, timeouts, headless, storage settings
├── pages/                     # Page Object Models
│   └── chatbot_page.py
├── data/                      # Data-driven test inputs
│   └── test_data.json         # Prompts, expected keywords, thresholds
├── utils/                     # Helpers: reporting, AI comparison, payloads
│   ├── reporting.py           # Step context manager & reporting utilities
│   ├── ai_compare.py          # Keyword & semantic similarity checks
│   └── injection_payloads.py  # XSS/SQL/test payloads
├── scripts/                   # One-time setup scripts
│   └── setup_session.py       # Solve CAPTCHA & persist storage_state.json
├── tests/
│   ├── test_ui/               # UI behavior tests
│   │   └── test_chat_ui.py
│   ├── test_ai/               # AI response validation tests
│   │   └── test_chat_ai.py
│   └── test_security/         # Security & injection tests
│       └── test_chat_security.py
├── report/                    # Allure output directory
│   └── allure-results/
├── README.md                  # This file
└── pytest.ini                 # Pytest configuration (markers, pythonpath)
```

---

## ⚙️ Prerequisites

1. **Python 3.10+**, pip
2. **Playwright** browsers
3. **Allure** command-line tool

```bash
# Create & activate virtual environment (macOS/Linux)
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install Allure (macOS)
brew install allure
# Or on Linux
sudo apt-get install allure
```

---

## 🔐 One-Time Setup: CAPTCHA Bypass

On each network (home, office, etc.), run the setup script to manually solve any reCAPTCHA and persist session state:

```bash
python utils/setup_session.py
python -m utils.setup_session
```

This opens a headful browser, lets you solve the CAPTCHA, then saves `storage/auth.json`. Subsequent test runs will reuse this session to avoid further challenges.

---

## 🧪 Running Tests

By default, tests run in **headful** mode for debugging. You can override via environment variables.

```bash
# Run all UI tests only
pytest tests/test_ui --alluredir=report/allure-results

# Run all tests
pytest tests --alluredir=report/allure-results
```

### Environment Variables

* `UASK_LANG` ("en" or "ar"). Defaults to `en`.
* `HEADLESS` (`true` or `false`). Defaults to `false` (visible browser).
* `ALLURE_DIR` (path for Allure results). Defaults to `report/allure-results`.

Example:

```bash
export UASK_LANG=ar
export HEADLESS=true
pytest tests --alluredir=$ALLURE_DIR
```

---

## 📊 Viewing Reports

After running tests, generate and view the Allure report:

```bash
allure serve report/allure-results
```

This launches an interactive dashboard with:

* Test overview (passed/failed)
* Step-by-step logs and attachments
* Screenshots for every step and failures
* Traces and videos (if enabled)

---

## 📝 Test Suite Organization

### 1. UI Behavior Tests (`test_ui`)

* Widget visibility on Desktop/Mobile
* Message send/receive
* Input clearing
* Layout direction (LTR/RTL)
* Scrolling and accessibility checks

### 2. AI Response Validation (`test_ai`)

* Data-driven prompts from `data/test_data.json`
* Keyword presence and semantic thresholds
* Consistency between English/Arabic
* Clean formatting (no broken HTML)
* Fallback messages under simulated API failures

### 3. Security Tests (`test_security`)

* XSS sanitization (`<script>` tags)
* Prompt injection resistance
* SQL-style and other malicious payloads

---

## 💡 Tips & Best Practices

* **Page Object Model** centralizes selectors and actions.
* **Allure `step()` context manager** captures screenshots automatically per step.
* **pytest markers** (`@pytest.mark.ui`, `@pytest.mark.ai`, `@pytest.mark.sec`) help filter tests.
* **CI Integration**: set `HEADLESS=true` and publish `report/allure-results` as an artifact.

---

Happy testing! 🚀
