import yfinance as yf
import pandas as pd
import ta
import time
from datetime import datetime, timedelta
from telegram import Bot

TOKEN = "8624976070:AAHSu9J8ouPdOgQV185hEBnAaJzVd13lxgQ"
CHAT_ID = "8605692810"

bot = Bot(token=TOKEN)

pares = ["EURUSD=X","GBPUSD=X","USDJPY=X","EURJPY=X","AUDUSD=X"]

def analisar(par):

    df = yf.download(par, interval="5m", period="1d")

    if df.empty or len(df) < 60:
        return None,0

    close = df["Close"]

    rsi = ta.momentum.RSIIndicator(close,14).rsi().iloc[-1]

    macd = ta.trend.MACD(close).macd_diff().iloc[-1]

    ema50 = ta.trend.EMAIndicator(close,50).ema_indicator().iloc[-1]

    bb = ta.volatility.BollingerBands(close)

    lower = bb.bollinger_lband().iloc[-1]
    upper = bb.bollinger_hband().iloc[-1]

    preco = close.iloc[-1]

    score = 0

    if rsi < 30:
        score += 1
    if macd > 0:
        score += 1
    if preco > ema50:
        score += 1
    if preco <= lower:
        score += 1

    if score >= 3:
        return "CALL", score

    score = 0

    if rsi > 70:
        score += 1
    if macd < 0:
        score += 1
    if preco < ema50:
        score += 1
    if preco >= upper:
        score += 1

    if score >= 3:
        return "PUT", score

    return None,0


while True:

    for par in pares:

        sinal,score = analisar(par)

        if sinal:

            entrada = datetime.now() + timedelta(minutes=5)

            hora = entrada.strftime("%H:%M")

            msg = f"""
🔥 OTC MASTER PRO

Par: {par}
Entrada: {sinal}
Expiração: M5

Entrar na vela: {hora}
Força do sinal: {score*25}%
"""

            bot.send_message(chat_id=CHAT_ID,text=msg)

    time.sleep(300)
