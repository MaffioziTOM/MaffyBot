import os
from telegram import Bot, Update
from telegram import constants
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackContext, filters

# 🔹 Загружаем переменные окружения (используйте свои значения)
TOKEN = "7965432987:AAFQqeT79_vO6YFh3s2hXTZxbJStLJ9HHe0"  # Токен вашего бота от BotFather
CHANNEL_ID = "-1002468008518"  # ID вашего канала (например, "-1002468008518")
ADMIN_ID = "752269181"  # Ваш личный Telegram ID (узнать можно через @userinfobot)

# Создаём объект бота
bot = Bot(token=TOKEN)

# 🔹 Функция обработки команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("**✨ Привет, искатель тайн! ✨\n\n💬 Отправляй свой вопрос, пока бот не ушёл в творческий кризис!\n(Шанс на ответ +100%, если подойдёшь с душой, а не с «когда прода?» 😏)\n\n✨ Дерзай! Кто спрашивает — тот познаёт!**")

# 🔹 Функция обработки сообщений от пользователей
async def handle_message(update: Update, context: CallbackContext):
    # Проверяем, что сообщение не от администратора
    if str(update.message.from_user.id) == ADMIN_ID:
        return  # Игнорируем сообщения от администратора

    question = update.message.text

    # Отправляем вопрос администратору
    await bot.send_message(chat_id=ADMIN_ID, text=f"💬 Новый вопрос:\n{question}\n\nОтветь мне в ЛС, чтобы отправить ответ в канал!")

    # Отвечаем пользователю
    await update.message.reply_text("**💌 Доставлено! Маффи уже смотрит на твой вопрос с задумчивым «хммм»…**")

    # Сохраняем вопрос в контексте
    context.user_data['last_question'] = question

# 🔹 Функция обработки ответов от администратора
async def handle_admin_reply(update: Update, context: CallbackContext):
    # Проверяем, что сообщение от администратора
    if str(update.message.from_user.id) != ADMIN_ID:
        return  # Игнорируем сообщения не от администратора

    answer = update.message.text
    question = context.user_data.get('last_question', 'Неизвестный вопрос')

    # Форматируем сообщение
    formatted_message = (
        f"**👤 Аноним:**\n"
        f"— *{question}*\n\n"
        f"**🎤 Маффи:**\n"
        f"— *{answer}*\n\n"
        f"**💌 Тоже есть вопрос? Бот всегда ждёт! 👉 @ask_maffi_bot**"
    )

    # Отправляем ответ в канал
    await bot.send_message(chat_id=CHANNEL_ID, text=formatted_message, parse_mode=constants.ParseMode.MARKDOWN)

    await update.message.reply_text("Ответ отправлен в канал!")

# 🔹 Создаём приложение бота
application = Application.builder().token(TOKEN).build()

# 🔹 Добавляем обработчики команд и сообщений
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_admin_reply))

# 🔹 Запускаем бота
if __name__ == "__main__":
    application.run_polling()
