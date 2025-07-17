from requests_html import HTMLSession
from telegram import Bot
import os
import time

SEARCH = "shirt"
MAX_PRICE = 30
VINTED_URL = f"https://www.vinted.it/vetements?search_text={SEARCH}"
seen = set()

bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def check_vinted():
    session = HTMLSession()
    r = session.get(VINTED_URL)
    r.html.render(timeout=30)

    items = r.html.find("a[href^='/items/']")
    print(f"Trovati {len(items)} articoli")

    for item in items:
        href = item.attrs["href"]
        if href in seen:
            continue
        seen.add(href)

        price_span = item.find("span[class*=Price__amount]", first=True)
        if not price_span:
            continue
        price_text = price_span.text.replace("€", "").replace(",", ".").strip()
        try:
            price = float(price_text)
        except:
            continue

        if price <= MAX_PRICE:
            link = "https://www.vinted.it" + href
            bot.send_message(chat_id=CHAT_ID, text=f"🛍️ Prodotto trovato a {price}€\n{link}")

while True:
    try:
        check_vinted()
    except Exception as e:
        print("Errore:", e)
    time.sleep(60)
