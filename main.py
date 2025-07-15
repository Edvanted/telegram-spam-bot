import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "123456789:ABCdefGhIJKlmnoPQRstuVwxyz1234567890"
WHITELIST = ["mrgrgrv", "sbleskom_manager"]

STOPWORDS = [
    "заработок", "выиграй", "казино", "деньги", "доход", "инвестиции", "прибыль",
    "криптовалюта", "бинанс", "ставки", "телеграм бот", "переходи", "вступай",
    "акция", "рассылка", "подпишись", "купи", "продам", "даром", "скидка", "бонус",
    "гарантия", "лёгкие деньги", "1xbet", "ставка", "биткойн", "forex", "crypto",
    "успей", "услуги", "услуга", "разблокировать", "бесплатно", "обнажёнка", "эротика",
    "секс", "18+", "порно", "porn", "xnxx", "xxx", "попрошайка", "help me", "нужна помощь",
    "donate", "донат", "qiwi", "кошелёк", "соберите", "сбор", "пожертвование", "молитва"
]

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message

    if user and user.username in WHITELIST:
        return

    text = (message.text or message.caption or "").lower()

    if any(word in text for word in STOPWORDS) or "http" in text or "t.me/" in text or "@" in text:
        await message.delete()
        logging.info(f"❌ Удалено сообщение от @{user.username if user else 'Unknown'}: {text}")

if __name__ == "__main__":
    print("✅ Бот успешно запущен и фильтрует спам...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    app.run_polling()
