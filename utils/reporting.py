import allure
from contextlib import contextmanager

@contextmanager
def step(name: str, page):
    """
    Wrap an Allure step and automatically capture + attach a screenshot
    inside the step block (whether it passed or failed).
    """
    with allure.step(name):
        try:
            yield
        finally:
            png = page.screenshot(full_page=True)
            allure.attach(
                png,
                name=f"{name} — screenshot",
                attachment_type=allure.attachment_type.PNG
            )


def attach_screenshot(name: str, page):
    """
    Capture a full-page screenshot and attach it to the Allure report.
    """
    png = page.screenshot(full_page=True)
    allure.attach(
        png,
        name=name,
        attachment_type=allure.attachment_type.PNG
    )