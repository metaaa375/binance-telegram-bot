import asyncio
import os
import time
import requests
from flask import Flask
from telegram import Bot

# ⚠️ Variables d'environnement à configurer sur Render :
# TELEGRAM_TOKEN = ton token du bot
# CHAT_ID = ton chat_id Telegram

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot Binance Listings tourne en continu !"

# URL Binance : section New Cryptocurrency Listings
BINANCE_URL = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
PARAMS = {"type": 1, "catalogId": 48, "pageNo": 1, "pageSize": 5}

# Stockage en mémoire du dernier code déjà envoyé
last_seen_code = None

def fetch_binance_announcements():
    """Récupère les dernières annonces Binance."""
    try:
        resp = requests.get(BINANCE_URL, params=PARAMS, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        articles = data.get("data", {}).get("articles", [])
        return articles if articles else []

    except Exception as e:
        print(f"⚠️ Erreur lors de la récupération : {e}")
        return []

def check_new_announcements():
    """Vérifie s'il y a une nouvelle annonce et envoie un message."""
    global last_seen_code
    articles = fetch_binance_announcements()

    if not articles:
        print("⚠️ Aucune annonce trouvée.")
        return

    latest = articles[0]  # la plus récente
    latest_code = latest.get("code")
    latest_title = latest.get("title", "Sans titre")
    latest_url = "https://www.binance.com/en/support/announcement/" + latest_code

    if last_seen_code != latest_code:
        # ⚡ Nouvelle annonce détectée
        message = f"🚨 Nouvelle annonce Binance :\n\n📌 {latest_title}\n🔗 {latest_url}"
        asyncio.run(bot.send_message(chat_id=CHAT_ID, text=message))
        last_seen_code = latest_code
        print("✅ Nouvelle annonce envoyée :", latest_title)
    else:
        print("ℹ️ Pas de nouvelle annonce.")

if __name__ == "__main__":
    print("🚀 Bot Binance lancé et surveille toutes les minutes...")
    while True:
        check_new_announcements()
        time.sleep(60)  # vérifie toutes les minutes




