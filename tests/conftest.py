# tests/conftest.py

import os
import pytest
import allure
from playwright.sync_api import sync_playwright
from config.config import HEADLESS, TRACE_RESULTS_DIR, STORAGE_STATE_PATH
from utils.logger import LOG_STREAM


@pytest.fixture(scope="session")
def browser():
    """
    Launch a single Playwright browser instance for the session.
    """
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=HEADLESS)
    yield browser
    pw.stop()


@pytest.fixture(scope="function")
def context(browser, request):
    """
    Create a new context per test, reusing the saved storageState for CAPTCHA bypass,
    stub out grecaptcha, and start tracing.
    """
    if not os.path.exists(STORAGE_STATE_PATH):
        raise RuntimeError(
            "Missing session storage. Run `python utils/setup_session.py` first."
        )
    ctx = browser.new_context(
        storage_state=STORAGE_STATE_PATH,
        viewport={"width": 1280, "height": 800},
        locale="en-US",
        timezone_id="Asia/Dubai",
    )

    # Stub out Recaptcha so it never appears
    ctx.add_init_script(
        """
      window.grecaptcha = {
        ready: (cb) => cb(),
        execute: () => Promise.resolve('TEST_TOKEN')
      };
    """
    )

    # Start tracing (screenshots, snapshots, sources)
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx

    # Stop tracing to a zip file
    trace_path = os.path.join(TRACE_RESULTS_DIR, f"{request.node.name}.zip")
    ctx.tracing.stop(path=trace_path)
    ctx.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    After each test call, attach detailed logs and, on failure, a screenshot to Allure.
    """
    outcome = yield
    report = outcome.get_result()

    # Attach logs for every test, regardless of pass/fail
    LOG_STREAM.seek(0)
    log_contents = LOG_STREAM.read()
    if log_contents:
        allure.attach(
            log_contents,
            name=f"{item.name} – logs",
            attachment_type=allure.attachment_type.TEXT,
        )
    # Clear buffer for next test
    LOG_STREAM.truncate(0)
    LOG_STREAM.seek(0)

    # If the test failed, also attach a full-page screenshot
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            png = page.screenshot(full_page=True)
            allure.attach(
                png,
                name=f"{item.name} – failure screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
