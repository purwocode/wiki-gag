import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === CONFIG ===
TELEGRAM_BOT_TOKEN = "8470224290:AAG_qI3sWUWe4FJ6h37EwkQYt06x_y1ZuA8"
BASE_URL = "https://growagarden.fandom.com/wiki/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/139.0.0.0 Safari/537.36"
}

# === LOGGING ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# === LABEL DATA ===
LABELS = {
    2: "Metode Perolehan",
    3: "Peluang Didapatkan",
    4: "Skill Pasif",
    5: "Harga",
    6: "Tingkat Kelaparan",
    7: "Dapat Diperoleh",
    8: "Tanggal Ditambahkan"
}


# === SCRAPER ===
def scrape_pet(pet_name: str) -> str:
    url = BASE_URL + pet_name.replace(" ", "_")
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return f"❌ Gagal mengakses halaman {pet_name}"

    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.find_all("div", class_="pi-data-value pi-font")

    if not divs:
        return f"❌ Data untuk {pet_name} tidak ditemukan."

    result = [f"📖 *{pet_name}*"]
    for i, div in enumerate(divs, start=1):
        text = div.get_text(strip=True)
        if i in LABELS:
            result.append(f"➡️ {LABELS[i]} : {text}")

    return "\n".join(result)


# === HANDLER ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo Mek! Kirimkan nama pet dengan perintah:\n"
                                    "`/pet Red Fox`", parse_mode="Markdown")


async def pet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Masukin Nama Pet yang bener Njeng. Contoh: `/pet Red Fox`",
                                        parse_mode="Markdown")
        return

    pet_name = " ".join(context.args)
    result = scrape_pet(pet_name)
    await update.message.reply_text(result, parse_mode="Markdown")


# === MAIN ===
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pet", pet))

    print("Bot berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
