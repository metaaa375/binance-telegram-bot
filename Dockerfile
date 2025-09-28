# On force Python 3.12 pour garder imghdr
FROM python:3.12-slim

# Répertoire de travail
WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code
COPY . .

# Lancer ton bot
CMD ["python", "bot_binance_test.py"]
