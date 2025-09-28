import requests
import schedule
import time
from telegram import Bot

# Ton token de bot et ton chat_id
BOT_TOKEN = "8271380593:AAEgKCuQluAOXYujVECjDZ2y698_rKLNNTc"
CHAT_ID = 420284200  # Ton chat ID
bot = Bot(token=BOT_TOKEN)

def fetch_binance_announcements():
    """Récupère les 5 dernières annonces Binance (nouvelles cryptos listées)."""
    url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
    params = {
        "type": 1,
        "catalogId": 48,  # Section "New Cryptocurrency Listings"
        "pageNo": 1,
        "pageSize": 5
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("data", {}).get("articles", [])
            return articles
        else:
            return None
    except Exception as e:
        print("Erreur:", e)
        return None

def send_daily_update():
    """Envoie un message Telegram avec les 5 dernières annonces."""
    articles = fetch_binance_announcements()
    if articles:
        message = "📢 Dernières annonces Binance (listings) :\n\n"
        for art in articles:
            title = art.get("title", "Sans titre")
            link = "https://www.binance.com/fr/support/announcement/" + art.get("code", "")
            message += f"- {title}\n{link}\n\n"
        bot.send_message(chat_id=CHAT_ID, text=message)
    else:
        bot.send_message(chat_id=CHAT_ID, text="⚠️ Impossible de trouver les annonces Binance.")

if __name__ == "__main__":
    # ⚡ ENVOI DE TEST IMMÉDIAT
    send_daily_update()

    # Programmation : tous les jours à 09h00
    schedule.every().day.at("09:00").do(send_daily_update)

    print("✅ Bot démarré et en attente.
