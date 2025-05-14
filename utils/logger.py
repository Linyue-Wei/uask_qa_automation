import logging
import io

LOG_STREAM = io.StringIO()

handler = logging.StreamHandler(LOG_STREAM)
handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)
logging.root.setLevel(logging.DEBUG)
logging.root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
