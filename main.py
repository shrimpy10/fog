#!/usr/bin/env python3
import os, random, requests, logging

# ——— CONFIG —————————————————————
BOT_TOKEN   = "7053656993:AAH1THmz8dRotjYErpQCrH6d39oFfnvUyw4"
CHAT_ID     = "-1002673571949"
MEME_FOLDER = "./memes"  
# ————————————————————————————————

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

# pick one at random
memes = os.listdir(MEME_FOLDER)
if not memes:
    logger.error("No memes found")
    exit(1)
choice = random.choice(memes)
path = os.path.join(MEME_FOLDER, choice)

# send it
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
with open(path, "rb") as f:
    r = requests.post(
        url,
        data={"chat_id": CHAT_ID},
        files={"photo": f},
        timeout=30
    )
if r.ok:
    logger.info("✅ Sent %s", choice)
else:
    logger.error("❌ Telegram error: %s", r.text)
