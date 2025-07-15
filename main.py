from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = '7382250158:AAE6DLfyjuTK-PmCAgDc9H9_7Tk0uKvNBto'

BAD_WORDS = [
    "http", "https", "t.me", "@", "подпишись", "скидка", "продажа",
    "заработок", "деньги", "вк", "кликни", "регистрация", "чат"
]

WHITELIST_USERNAMES = ['mrgrgrv', 'sbleskom_manager']

async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    if message.sender_chat:
        print(f"✅ Пропущено: сообщение от имени группы — {message.sender_chat.title}")
        return

    user = message.from_user
    user_id = user.id
    username = user.username or ""

    text = message.text.lower()
    chat_id = message.chat_id

    try:
        chat_admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in chat_admins]
    except Exception as e:
        print(f"⚠️ Не удалось получить админов: {e}")
        admin_ids = []

    if user_id in admin_ids or username in WHITELIST_USERNAMES:
        print(f"✅ Пропущено: @{username or user_id} — админ или в белом списке")
        return

    if any(bad in text for bad in BAD_WORDS):
        try:
            await message.delete()
            print(f"🚫 Удалено сообщение от @{username or user_id}: {text}")
        except Exception as e:
            print("❌ Ошибка удаления:", e)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_spam))
    print("🤖 Бот запущен. Фильтрует спам...")
    app.run_polling()
