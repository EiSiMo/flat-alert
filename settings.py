from dotenv import load_dotenv
from os import getenv

LANGUAGE: str = "de"
TIME_INTERVALL = 60

# secrets
load_dotenv()
GMAPS_API_KEY = getenv("GMAPS_API_KEY")
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = getenv("TELEGRAM_CHAT_ID")
BERLIN_WOHNEN_USERNAME = getenv("BERLIN_WOHNEN_USERNAME")
BERLIN_WOHNEN_PASSWORD = getenv("BERLIN_WOHNEN_PASSWORD")