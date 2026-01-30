import logging

import requests
from settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger("flat-alert (telegram.py)")

class Telegram:
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID

    def send_message(self, msg):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": msg,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            logger.error(f"failed to send telegram message: {e}")
