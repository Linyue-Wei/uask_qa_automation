import random
import time
from playwright.sync_api import Page, TimeoutError as PlaywrightTO, Locator
from config.config import DEFAULT_TIMEOUT, SHORT_TIMEOUT
from utils.logger import get_logger

class ChatbotPage:
    # ——— UI text / i18n ——————————————————————————————
    UI_TEXT = {
        "en": {
            "accept":       "Accept and continue",
            "lang_btn":     "العربية",
            "samples":      "Sample questions",
            "terms":        "Terms of Service",
            "send":         "Send",
            "default_q":    "What is the golden visa?",
            "scroll_q":     "What is the golden visa?",
            "expected_dir": "ltr"
        },
        "ar": {
            "accept":       "قبول ومتابعة",
            "lang_btn":     "English",
            "samples":      "عيّنة من أسئلة",
            "terms":        "شروط الخدمة",
            "send":         "إرسال",
            "default_q":    "ما هي متطلبات الحصول على تأشيرة الإقامة الذهبية؟",
            "scroll_q":     "ما هي متطلبات الحصول على تأشيرة الإقامة الذهبية؟",
            "expected_dir": "rtl"
        }
    }

    # ——— CSS selectors ————————————————————————————————————————
    _SEL = {
        "logo":       "role=link[name='Logo']",
        "lang_btn":   "role=button[name='{lang_btn}']",
        "accept_btn": "role=button[name='{accept}']",
        "samples":    "text={samples}",
        "input":      ".expando-textarea",
        "send_btn":   "role=button[name='{send}']",
        "mic_btn":    "role=button >> nth=2",
        "combo":      "role=combobox",
        "terms":      "role=link[name='{terms}']",
        "user_msgs":  ".chat-item.chat-message-out .chat-text.chat-message-text",
        "bot_msgs":   ".chat-item.chatbot.chat-message-in .chat-text.chat-message-text",
        "bot_conts":  ".chat-item.chatbot.chat-message-in",
        "msg_time":   ".chat-datetime.date-time",
        "role_log":   "[role=log]",
        "aria_label": "textarea[aria-label]"
    }

    # Pattern for sample questions
    SAMPLE_Q_PATTERN = "#chat-welcome-tab div.question:has-text('{}')"

    def __init__(self, page: Page, lang: str = "en"):
        self.page = page
        self.lang = lang
        self.text = self.UI_TEXT[lang]
        self.logger = get_logger(self.__class__.__name__)

        # Format selectors with UI text
        self.sel = {
            name: tpl.format(**self.text)
            for name, tpl in self._SEL.items()
        }

        # Prepare sample-question locators
        sample_texts = {
            "en": ["golden visa", "driving license", "sponsoring visa"],
            "ar": ["تأشيرة الإقامة الذهبية", "رخصة قيادة", "تأشيرة إقامة للأسرة"]
        }[lang]
        self.sample_q_locators = [
            page.locator(self.SAMPLE_Q_PATTERN.format(q))
            for q in sample_texts
        ]

        self.logger.debug(f"Initialized ChatbotPage (lang={lang})")

    def _wait_visible(self, target, name: str = None, timeout: int = SHORT_TIMEOUT) -> bool:
        """
        Wait up to `timeout` ms for either:
          - a CSS selector string, or
          - a Locator
        to become visible.
        """
        locator = target if isinstance(target, Locator) else self.page.locator(target)
        try:
            locator.wait_for(state="visible", timeout=timeout)
            if name:
                self.logger.debug(f"[OK] Visible: {name}")
            return True
        except PlaywrightTO:
            if name:
                self.logger.warning(f"[FAIL] Not visible within {timeout}ms: {name}")
            return False

    # ——— Page actions —————————————————————————————————————————————

    def open(self, url: str):
        self.logger.debug(f"Navigating to {url}")
        self.page.goto(url, timeout=DEFAULT_TIMEOUT)
        self.page.wait_for_load_state("networkidle", timeout=DEFAULT_TIMEOUT)
        self.logger.debug("Page loaded (network idle)")

    def accept_cookies(self):
        sel = self.sel["accept_btn"]
        self.logger.debug("Attempting to accept cookies")
        if self._wait_visible(sel, "Accept cookies"):
            self.page.click(sel)

    def send_message(self, msg: str = None):
        text = msg or self.text["default_q"]
        self.logger.debug(f"Sending message: {text!r}")
        self.page.click(self.sel["input"])
        for ch in text:
            time.sleep(random.uniform(0.08, 0.15))
            self.page.keyboard.type(ch)
        time.sleep(random.uniform(0.5, 1.2))
        self.page.keyboard.press("Enter")

    def wait_for_response(self, timeout: int = DEFAULT_TIMEOUT):
        sel = self.sel["bot_msgs"]
        self.logger.debug("Waiting for AI response text")
        self.page.wait_for_selector(sel, timeout=timeout)

    # ——— Verifications & data getters —————————————————————————————————

    def verify_main_elements_loaded(self) -> bool:
        """
        Quick‐fail check that all key UI controls are visible.
        """
        checks = [
            (self.sel["logo"],    "Logo"),
            (self.sel["lang_btn"],"Language toggle"),
            (self.sel["samples"], "Sample questions label"),
            (self.sel["input"],   "Input box"),
            (self.sel["send_btn"],"Send button"),
            (self.sel["mic_btn"], "Microphone button"),
            (self.sel["combo"],   "Language combobox"),
            (self.sel["terms"],   "Terms link"),
        ]
        for idx, locator in enumerate(self.sample_q_locators, start=1):
            checks.append((locator, f"Sample question #{idx}"))

        all_ok = True
        for target, name in checks:
            all_ok &= self._wait_visible(target, name)

        self.logger.debug(f"verify_main_elements_loaded → {all_ok}")
        return all_ok

    def get_all_bot_messages(self) -> list[str]:
        texts = self.page.locator(self.sel["bot_msgs"]).all_text_contents()
        clean = [t.strip() for t in texts if t.strip()]
        self.logger.debug(f"All bot messages: {clean}")
        return clean

    def get_last_bot_message(self) -> str:
        msgs = self.get_all_bot_messages()
        last = msgs[-1] if msgs else ""
        self.logger.debug(f"Last bot message: {last!r}")
        return last

    def input_is_cleared(self) -> bool:
        content = self.page.locator(self.sel["input"]).text_content() or ""
        cleared = not content.strip()
        self.logger.debug(f"Input cleared: {cleared}")
        return cleared

    def get_last_message_direction(self) -> str:
        cls = self.page.locator(self.sel["bot_conts"]).last.get_attribute("class") or ""
        direction = "rtl" if "rtl" in cls.split() else "ltr"
        self.logger.debug(f"Last message direction: {direction}")
        return direction

    def scroll_required(self) -> bool:
        area = self.page.locator(".chat-msg-history.scroll-container")
        req = area.evaluate("el => el.scrollHeight > el.clientHeight")
        self.logger.debug(f"Scroll required: {req}")
        return req

    def has_accessibility_roles(self) -> bool:
        ok = (
            self.page.locator(self.sel["role_log"]).is_visible(timeout=DEFAULT_TIMEOUT)
            and self.page.locator(self.sel["aria_label"]).count() > 0
        )
        self.logger.debug(f"Accessibility roles present: {ok}")
        return ok

    def get_message_timestamp(self, container_locator) -> str:
        ts = container_locator.locator(self.sel["msg_time"]).text_content().strip()
        self.logger.debug(f"Message timestamp: {ts}")
        return ts

    def get_user_messages(self) -> list[str]:
        texts = self.page.locator(self.sel["user_msgs"]).all_text_contents()
        clean = [t.strip() for t in texts if t.strip()]
        self.logger.debug(f"User messages: {clean}")
        return clean
