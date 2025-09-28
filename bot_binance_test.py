import threading
import asyncio
from flask import Flask
from telegram import Bot
import os
import schedule
import time
import requests

# ⚠️ Variables d'environnement à configurer sur Render :
# TELEGRAM_TOKEN = ton token du bot
# CHAT_ID = ton chat_id Telegram

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot Binance Listings tourne sur Render gratuitement !"

# Fonction pour récupérer les annonces Binance
def fetch_binance_announcements():
    url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
    params = {"type": 1, "catalogId": 48, "pageNo": 1, "pageSize": 5}  # section New Cryptocurrency Listings

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        articles = data.get("data", {}).get("articles", [])
        if not articles:
            return ["⚠️ Aucune annonce trouvée."]

        messages = []
        for art in articles:
            title = art.get("title", "Sans titre")
            link = "https://www.binance.com/en/support/announcement/" + art.get("code", "")
            messages.append(f"🆕 {title}\n🔗 {link}")

        return messages

    except Exception as e:
        return [f"⚠️ Erreur lors de la récupération : {e}"]

# Fonction qui envoie les annonces
def job():
    annonces = fetch_binance_announcements()
    for msg in annonces:
        asyncio.run(bot.send_message(chat_id=CHAT_ID, text=msg))

# Scheduler : 1 fois par jour à 9h (UTC)
schedule.every().day.at("09:00").do(job)
schedule.every().day.at("12:00").do(job)
schedule.every().day.at("15:00").do(job)
schedule.every().day.at("21:00").do(job)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # ⚡ Envoi immédiat au démarrage
    job()

    # Thread séparé pour exécuter le scheduler
    threading.Thread(target=run_schedule, daemon=True).start()

    # Flask maintient le service "vivant" pour Render



