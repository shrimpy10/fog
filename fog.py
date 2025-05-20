#!/usr/bin/env python3
import os
import time
import requests
import logging
import random

# ————— CONFIGURATION —————
BOT_TOKEN   = "7053656993:AAH1THmz8dRotjYErpQCrH6d39oFfnvUyw4"
CHAT_ID     = "-1002673571949"
MEME_FOLDER = "./memes"        # path to your folder of images
INTERVAL    = 3 * 60           # seconds between posts (3 minutes)
# ——————————————————————————

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def send_photo(path):
    """Send a single photo at `path` to the configured chat."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        with open(path, "rb") as img:
            files = {"photo": img}
            data = {"chat_id": CHAT_ID}
            resp = requests.post(url, data=data, files=files, timeout=30)
        resp.raise_for_status()
        logger.info("✅ Sent %s", os.path.basename(path))
    except Exception as e:
        logger.error("❌ Failed to send %s: %s", os.path.basename(path), e)

def main():
    # 1) Validate config
    if not os.path.isdir(MEME_FOLDER):
        logger.error("Meme folder not found: %s", MEME_FOLDER)
        return

    # 2) Load memes
    memes = os.listdir(MEME_FOLDER)
    random.shuffle(memes)                   # ← shuffle here
    logger.info("Shuffled meme order")
    if not memes:
        logger.error("No files in %s", MEME_FOLDER)
        return
    logger.info("Loaded %d memes from %s", len(memes), MEME_FOLDER)

    idx = 0
    # 3) Main loop
    while True:
        meme_path = os.path.join(MEME_FOLDER, memes[idx])
        send_photo(meme_path)

        # advance index, wrap around
        idx = (idx + 1) % len(memes)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
