import json
import pytest
import allure
from pages.chatbot_page import ChatbotPage
from config.config import LANG, BASE_URL
from utils.reporting import step


with open("data/test_security.json", encoding="utf-8") as f:
    TEST_CASES = json.load(f)

@pytest.mark.sec
@allure.epic("U-Ask Chatbot")
@allure.feature("Security & Injection Handling")
@pytest.mark.parametrize("case", TEST_CASES)
def test_security_and_injection(context, case):
    page = context.new_page()
    bot  = ChatbotPage(page, lang=LANG)

    with step(f"{case['name']} › Open & accept cookies", page):
        bot.open(BASE_URL)
        bot.accept_cookies()

    with step(f"{case['name']} › Send payload", page):
        bot.send_message(case["payload"])

    with step(f"{case['name']} › Wait for rendering & response", page):
        bot.wait_for_response()

    # 1) Sanitization: user message should appear verbatim (not executed)
    if case["type"] == "sanitization":
        users = bot.get_user_messages()
        last_user = users[-1] if users else ""
        assert case["expect_user_shows"] in last_user, (
            f"Expected sanitized user text to include {case['expect_user_shows']!r}, got {last_user!r}"
        )

    # 2) Injection: AI must not comply—look for fallback keywords
    if case["type"] == "injection":
        reply = bot.get_last_bot_message().lower()
        # ensure it at least contains one of the safe/fallback indicators
        keywords = [kw.lower() for kw in case.get("expect_bot_contains", [])]
        assert any(kw in reply for kw in keywords), (
            f"Expected bot response to contain one of {keywords}, got {reply!r}"
        )

    page.close()
