import json, re, pytest, allure
from pages.chatbot_page import ChatbotPage
from config.config import LANG, get_base_url
from utils.reporting import step

with open("data/test_ai.json", encoding="utf-8") as f:
    CASES = json.load(f)

@pytest.mark.ai
@allure.epic("U-Ask Chatbot")
@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_ai_response_validation(context, case):
    # 1) Label by category + intent
    allure.dynamic.feature(f"{case['category'].title()} Queries")
    allure.dynamic.story(case["intent"])

    page = context.new_page()
    bot  = ChatbotPage(page, lang=LANG)

    with step("Open & accept cookies", page):
        bot.open(get_base_url())
        bot.accept_cookies()

    prompt = case["prompts"][LANG]
    with step(f"Send prompt: {prompt}", page):
        bot.send_message(prompt)

    with step("Wait for AI response", page):
        bot.wait_for_response()

    reply = bot.get_last_bot_message()
    lower = reply.lower()

    # 2) Fallback on error
    if case["validate"].get("fallback"):
        kws = case["expected_keywords"][LANG]
        assert any(k in lower for k in kws), f"Expected fallback keywords {kws}, got: {reply}"
        return

    # 3) No hallucination: must include at least one domain keyword
    if case["validate"].get("hallucination"):
        kws = case["expected_keywords"][LANG]
        assert kws and any(k.lower() in lower for k in kws), (
            f"Expected one of {kws}, got: {reply}"
        )

    # 4) Formatting checks
    if case["validate"].get("format_clean"):
        # no raw HTML tags
        assert not re.search(r"<\/?[a-z][^>]*>", reply), f"Found HTML in: {reply}"
        # not cut off mid-sentence (e.g. trailing '...')
        assert not reply.strip().endswith("..."), f"Incomplete formatting: {reply}"

    # 5) Cross-language consistency (optional)
    other = "ar" if LANG=="en" else "en"
    other_prompt = case["prompts"][other]
    with step(f"Cross-lang check: send {other_prompt}", page):
        page2 = context.new_page()
        bot2   = ChatbotPage(page2, lang=other)
        bot2.open(get_base_url()); bot2.accept_cookies()
        bot2.send_message(other_prompt); bot2.wait_for_response()
        other_reply = bot2.get_last_bot_message().lower()
        exp_kws = case["expected_keywords"][other]
        # require at least one equivalent keyword
        if exp_kws:
            assert any(k.lower() in other_reply for k in exp_kws), (
                f"Cross-lang missing {exp_kws} in: {other_reply}"
            )
        page2.close()

    page.close()
