from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import logging

# Токен бота
TOKEN = "7382250158:AAE6DLfyjuTK-PmCAgDc9H9_7Tk0uKvNBto"

# Разрешённые имена пользователей (Telegram usernames без "@")
WHITELIST = ["mrgrgrv", "sbleskom_manager"]

# Расширенный список стоп-слов
STOP_WORDS = [
    "заработок", "выиграй", "казино", "порно", "секс", "эротика", "онлайн казино", "играй", "платно",
    "donate", "донат", "пожертвование", "розыгрыш", "bit.ly", "t.me/joinchat", "xxx", "🔞", "free",
    "быстрые деньги", "инвестиции", "ставки", "букмекер", "crypto", "usdt", "btc", "porn", "onlyfans",
    "sex", "viagra", "отправь", "получи", "пополни", "перейди по ссылке", "adult", "анонимно", "девушки"
]

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message:
        return

    # Проверка — обычный пользователь
    if message.from_user and message.from_user.username:
        username = message.from_user.username.lower()
        if username in WHITELIST:
            return

    # Проверка — анонимный админ (от имени чата)
    if message.sender_chat:
        chat_admins = await message.chat.get_administrators()
        for admin in chat_admins:
            if admin.user and admin.user.username and admin.user.username.lower() in WHITELIST:
                return  # Если этот админ в списке — не трогаем сообщение

    # Проверка текста на стоп-слова и ссылки
    text = (message.text or message.caption or "").lower()

    # Условие: если есть стоп-слово ИЛИ ссылка, НО не наша ссылка
    if (
        any(word in text for word in STOP_WORDS)
        or (("http" in text or "t.me/" in text or "@" in text) and "sbleskom.ru" not in text)
    ):
        try:
            await message.delete()
            logging.info(f"❌ Удалено сообщение от: {text}")
        except Exception as e:
            logging.warning(f"Ошибка при удалении: {e}")

if __name__ == "__main__":
    print("✅ Бот успешно запущен и фильтрует спам…")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    app.run_polling()
