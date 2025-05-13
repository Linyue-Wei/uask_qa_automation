import pytest
import allure
from pages.chatbot_page import ChatbotPage
from config.config import LANG, get_base_url
from utils.reporting import step


@allure.epic("U-Ask Chatbot")
@allure.feature("UI Behavior")
@pytest.mark.parametrize("device", ["Desktop", "Mobile"])
def test_chat_ui_elements(context, device):
    """
    Verify the chat widget and main UI elements for the configured language
    on Desktop and Mobile.
    """
    page = context.new_page()
    if device == "Mobile":
        page.set_viewport_size({"width": 375, "height": 812})

    bot = ChatbotPage(page, lang=LANG)

    with step(f"{LANG.upper()} - {device} › Open & accept cookies", page):
        bot.open(get_base_url())
        bot.accept_cookies()

    with step(f"{LANG.upper()} - {device} › Verify main UI elements", page):
        assert (
            bot.verify_main_elements_loaded()
        ), f"UI elements failed to load for {LANG} on {device}"

    page.close()


@allure.feature("UI Behavior")
@pytest.mark.parametrize("device", ["Desktop", "Mobile"])
def test_send_and_receive_message(context, device):
    """
    Verify user can send a message and receive a non-empty AI response
    rendered in the conversation area.
    """
    page = context.new_page()
    if device == "Mobile":
        page.set_viewport_size({"width": 375, "height": 812})

    bot = ChatbotPage(page, lang=LANG)

    with step(f"{LANG.upper()} - {device} › Open & accept cookies", page):
        bot.open(get_base_url())
        bot.accept_cookies()

    with step(f"{LANG.upper()} - {device} › Send message", page):
        bot.send_message()

    with step(f"{LANG.upper()} - {device} › Wait for response", page):
        bot.wait_for_response()

    with step(f"{LANG.upper()} - {device} › Assert AI response is non-empty", page):
        reply = bot.get_last_bot_message()
        assert reply, f"Empty AI response for {LANG} on {device}"

    page.close()


@allure.feature("UI Behavior")
@pytest.mark.parametrize("device", ["Desktop", "Mobile"])
def test_input_clears_after_sending(context, device):
    """
    After sending, the input box should be cleared.
    """
    page = context.new_page()
    if device == "Mobile":
        page.set_viewport_size({"width": 375, "height": 812})

    bot = ChatbotPage(page, lang=LANG)

    with step(f"{LANG.upper()} - {device} › Open & accept cookies", page):
        bot.open(get_base_url())
        bot.accept_cookies()

    with step(f"{LANG.upper()} - {device} › Send message & wait", page):
        bot.send_message()
        bot.wait_for_response()

    with step(f"{LANG.upper()} - {device} › Assert input cleared", page):
        assert (
            bot.input_is_cleared()
        ), f"Input box was not cleared for {LANG} on {device}"

    page.close()


@allure.feature("UI Behavior")
@pytest.mark.parametrize("device", ["Desktop", "Mobile"])
def test_layout_direction(context, device):
    """
    Verify that responses render LTR for English and RTL for Arabic.
    """
    page = context.new_page()
    if device == "Mobile":
        page.set_viewport_size({"width": 375, "height": 812})

    bot = ChatbotPage(page, lang=LANG)

    with step(f"{LANG.upper()} - {device} › Open & accept cookies", page):
        bot.open(get_base_url())
        bot.accept_cookies()

    with step(f"{LANG.upper()} - {device} › Send message & wait", page):
        bot.send_message()
        bot.wait_for_response()

    with step(f"{LANG.upper()} - {device} › Assert layout direction", page):
        direction = bot.get_last_message_direction()
        expected = bot.text["expected_dir"]
        assert (
            direction == expected
        ), f"Expected '{expected}' for {LANG} on {device}, got '{direction}'"

    page.close()


@allure.feature("UI Behavior")
@pytest.mark.parametrize("device", ["Desktop", "Mobile"])
def test_scroll_and_accessibility(context, device):
    """
    Verify scrolling and accessibility roles work after multiple messages.
    """
    page = context.new_page()
    if device == "Mobile":
        page.set_viewport_size({"width": 375, "height": 812})

    bot = ChatbotPage(page, lang=LANG)

    with step(f"{LANG.upper()} - {device} › Open & accept cookies", page):
        bot.open(get_base_url())
        bot.accept_cookies()

    with step(f"{LANG.upper()} - {device} › Send multiple messages", page):
        for i in range(10):
            bot.send_message(msg=f"1+{i}=?")  
            bot.wait_for_response()

    with step(f"{LANG.upper()} - {device} › Assert scroll triggered", page):
        assert bot.scroll_required(), f"Scroll not triggered for {LANG} on {device}"

    with step(f"{LANG.upper()} - {device} › Assert accessibility roles", page):
        assert (
            bot.has_accessibility_roles()
        ), f"Accessibility roles missing for {LANG} on {device}"

    page.close()
