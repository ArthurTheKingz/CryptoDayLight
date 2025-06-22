from flask import Flask, request, jsonify, render_template
from threading import Thread
import requests
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Configurações
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
COINCAP_TOKEN = os.getenv("COINCAP_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', project_name="CryptoDayLight")

@app.route('/api/price', methods=['GET'])
def get_price():
    crypto = request.args.get('crypto')
    vs_currencies = ['usd', 'eur', 'brl']

    headers = {
        "Authorization": f"Bearer {COINCAP_TOKEN}"
    }

    url = f"https://api.coincap.io/v2/assets/{crypto.lower()}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json().get('data')
        if data:
            price_usd = float(data['priceUsd'])
            # Vamos usar uma API externa para câmbio USD -> EUR, BRL (exemplo rápido)
            exchange_rates = {
                "eur": get_exchange_rate("USD", "EUR"),
                "brl": get_exchange_rate("USD", "BRL")
            }
            price_eur = round(price_usd * exchange_rates["eur"], 4)
            price_brl = round(price_usd * exchange_rates["brl"], 4)

            return jsonify({
                'name': data['name'],
                'symbol': data['symbol'],
                'price_usd': round(price_usd, 4),
                'price_eur': price_eur,
                'price_brl': price_brl,
                'change24h': round(float(data['changePercent24Hr']), 2),
                'marketCap': round(float(data['marketCapUsd']), 2),
                'volume24h': round(float(data['volumeUsd24Hr']), 2)
            })
        else:
            return jsonify({'error': '❌ Criptomoeda não encontrada'}), 404
    else:
        return jsonify({'error': '❌ Erro na API CoinCap'}), 500

def get_exchange_rate(base, target):
    # Usando API gratuita de câmbio para taxas USD->EUR, USD->BRL
    try:
        url = f"https://api.exchangerate.host/latest?base={base}&symbols={target}"
        r = requests.get(url)
        rate = r.json().get("rates", {}).get(target, 1)
        return rate
    except:
        return 1

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🚀 Abra o CryptoDayLight aqui:",
        reply_markup={
            "inline_keyboard": [[
                {
                    "text": "🪙 Abrir Mini App",
                    "web_app": {"url": "https://seu-repl-nome.seunome.repl.co"}
                }
            ]]
        }
    )

keep_alive()

app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app_telegram.add_handler(CommandHandler("start", start))

print("✅ Bot rodando...")
app_telegram.run_polling()