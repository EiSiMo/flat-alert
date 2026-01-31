import os

DATA_DIR = "data"
ALREADY_NOTIFIED_FILE = "data/already_notified.txt"

# create dirs if they do not exist yet.
os.makedirs(DATA_DIR, exist_ok=True)