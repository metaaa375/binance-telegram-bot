import asyncio
import requests
import schedule
import time
from telegram import Bot

# ========================
# CONFIG
# ========================
TOKEN = "TON_TELEGRAM_BOT_TOKEN"   # <- remplace par ton vrai token
CHAT_ID = 420284200                # <- remplace par ton vrai chat_id
bot = Bot(token=TOKEN)


# ========================
# Récupération des annonces Binance
# ========================
def fetch_binance_announcements():
    url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
    params = {
        "type": 1,
        "catalogId": 48,  # Section "New Cryptocurrency Listings"
        "pageNo": 1,
        "pageSize": 5
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        articles = data.get("data", {}).get("articles", [])
        if not articles:
            return ["⚠️ Impossible de trouver les annonces Binance."]

        messages = []
        for article in articles:
            title = article.get("title", "Sans titre")
            link = "https://www.binance.com/en/support/announcement/" + article.get("code", "")
            messages.append(f"🆕 {title}\n🔗 {link}")

        return messages

    except Exception as e:
        return [f"❌ Erreur lors de la récupération : {e}"]


# ========================
# Envoi d’un message
# ========================
async def send_message(text):
    await bot.send_message(chat_id=CHAT_ID, text=text)


# ========================
# Tâche programmée
# ========================
async def job():
    announcements = fetch_binance_announcements()
    for msg in announcements:
        await send_message(msg)


# ========================
# Boucle principale
# ========================
async def scheduler():
    # Planifie l'envoi une fois par jour à 9h UTC
    schedule.every().day.at("09:00").do(lambda: asyncio.create_task(job()))

    # 🔥 Envoi immédiat au démarrage pour test
    await send_message("✅ Bot Binance démarré avec succès !")

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


if __name__ == "__main__":
    print("✅ Bot Binance lancé (Background Worker Render)...")
    asyncio.run(scheduler())


