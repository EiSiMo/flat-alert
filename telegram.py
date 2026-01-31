import logging

import requests
from settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger("flat-alert")

class Telegram:
    def send_message(self, msg):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            logger.error(f"failed to send telegram message: {e}")
