# utils/logger.py

import logging
import io

# 1) In-memory buffer for pytest Allure attachments:
LOG_STREAM = io.StringIO()

# 2) Configure root logger
handler = logging.StreamHandler(LOG_STREAM)
handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)
logging.root.setLevel(logging.DEBUG)
logging.root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
