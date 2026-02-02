from dotenv import load_dotenv
from os import getenv

load_dotenv()

LANGUAGE: str = getenv("LANGAUGE", "en")
TIME_INTERVALL: int = int(getenv("SLEEP_INTERVALL", "60"))

# secrets
GMAPS_API_KEY: str = getenv("GMAPS_API_KEY")
TELEGRAM_TOKEN: str = getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID: str = getenv("TELEGRAM_CHAT_ID")
BERLIN_WOHNEN_USERNAME: str = getenv("BERLIN_WOHNEN_USERNAME")
BERLIN_WOHNEN_PASSWORD: str = getenv("BERLIN_WOHNEN_PASSWORD")