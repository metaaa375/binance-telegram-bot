import requests
import schedule
import time
import asyncio
from telegram import Bot

# Ton token Telegram
TOKEN = "8271380593:AAEgKCuQluAOXYujVECjDZ2y698_rKLNNTc"
# Ton chat ID (met ton ID ou celui de ton groupe)
CHAT_ID = 420284200

bot = Bot(token=TOKEN)

def fetch_binance_announcements():
    """
    Récupère les 5 dernières annonces de la section
    'New Cryptocurrency Listings' de Binance.
    """
    url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
    params = {
        "type": 1,
        "catalogId": 48,   # Section New Cryptocurrency Listings
        "pageNo": 1,
        "pageSize": 5
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if "data" not in data or "articles" not in data["data"]:
            return []

        articles = data["data"]["articles"]
        results = []
        for art in articles:
            title = art.get("title", "Sans titre")
            link = "https://www.binance.com/en/support/announcement/" + art.get("code", "")
            results.append(f"🔔 {title}\n{link}")

        return results

    except Exception as e:
        print("Erreur lors de la récupération :", e)
        return []

async def send_daily_announcements():
    """
    Envoie les 5 dernières annonces sur Telegram.
    """
    announcements = fetch_binance_announcements()
    if not announcements:
        await bot.send_message(chat_id=CHAT_ID, text="⚠️ Impossible de trouver les annonces Binance.")
    else:
        message = "📢 Dernières annonces Binance :\n\n" + "\n\n".join(announcements)
        await bot.send_message(chat_id=CHAT_ID, text=message)

def job():
    asyncio.run(send_daily_announcements())

# Planifier l’envoi chaque jour à 10h
schedule.every().day.at("10:00").do(job)

print("🤖 Bot démarré et en attente...")

# Boucle infinie pour garder le bot actif
while True:
    schedule.run_pending()
    time.sleep(30)

