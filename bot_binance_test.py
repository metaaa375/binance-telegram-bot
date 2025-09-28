import requests
import time
import os
import telegram

# Config Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telegram.Bot(token=BOT_TOKEN)

# URL des annonces Binance
BINANCE_URL = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageNo=1&pageSize=5"

# Fichier pour stocker le dernier ID
LAST_ID_FILE = "last_id.txt"

def get_last_id():
    """Lire le dernier ID sauvegardé (si existe)."""
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_id(article_id):
    """Sauvegarder le dernier ID."""
    with open(LAST_ID_FILE, "w") as f:
        f.write(str(article_id))

def check_binance_announcements():
    try:
        response = requests.get(BINANCE_URL)
        data = response.json()

        articles = data["data"]["articles"]
        if not articles:
            print("⚠️ Aucune annonce trouvée.")
            return

        # On prend la plus récente
        latest = articles[0]
        latest_id = str(latest["id"])
        latest_title = latest["title"]
        latest_url = "https://www.binance.com/fr/support/announcement/" + latest["code"]

        last_id = get_last_id()

        if last_id != latest_id:  # Si c’est une nouvelle annonce
            message = f"🚨 Nouvelle annonce Binance :\n\n📌 {latest_title}\n🔗 {latest_url}"
            bot.send_message(chat_id=CHAT_ID, text=message)
            save_last_id(latest_id)
        else:
            print("✅ Pas de nouvelle annonce.")

    except Exception as e:
        print(f"⚠️ Erreur : {e}")

if __name__ == "__main__":
    while True:
        check_binance_announcements()
        time.sleep(60)  # Vérifie toutes les minutes
