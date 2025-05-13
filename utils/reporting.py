import allure
from contextlib import contextmanager


@contextmanager
def step(name: str, page):
    """
    Wrap an Allure step and automatically capture + attach a screenshot
    after the step block completes (whether it passed or failed).

    Usage:
        with step("Do something", page):
            # perform actions
    """
    with allure.step(name):
        yield
    # after step completes, capture screenshot
    png = page.screenshot(full_page=True)
    allure.attach(
        png,
        name=f"{name} — screenshot",
        attachment_type=allure.attachment_type.PNG
    )


def attach_screenshot(name: str, page):
    """
    Capture a full-page screenshot and attach it to the Allure report.

    Usage:
        attach_screenshot("Checkpoint name", page)
    """
    png = page.screenshot(full_page=True)
    allure.attach(
        png,
        name=name,
        attachment_type=allure.attachment_type.PNG
    )
