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
    await update.message.reply_text("Привет! Отправь мне анонимный вопрос, и я передам его автору.")

# 🔹 Функция обработки сообщений от пользователей
async def handle_message(update: Update, context: CallbackContext):
    question = update.message.text
    user_id = update.message.from_user.id  # Получаем ID пользователя
    username = update.message.from_user.username  # Получаем username пользователя (если есть)

    # Сохраняем данные в контексте
    context.user_data['last_question'] = {
        'question': question,
        'user_id': user_id,
        'username': username
    }

    # Отправляем вопрос администратору
    await bot.send_message(chat_id=ADMIN_ID, text=f"❓ Новый вопрос:\n{question}\n\nОтветь мне в ЛС, чтобы отправить ответ в канал!")

    # Отвечаем пользователю
    await update.message.reply_text("Спасибо! Ваш вопрос передан.")

# 🔹 Функция обработки ответов от администратора
async def handle_admin_reply(update: Update, context: CallbackContext):
    answer = update.message.text
    question_data = context.user_data.get('last_question', None)

    if not question_data:
        await update.message.reply_text("Ошибка: вопрос не найден.")
        return

    question = question_data['question']
    user_id = question_data['user_id']
    username = question_data.get('username', 'Аноним')

    # Форматируем сообщение
    formatted_message = (
        f"**👤 Аноним ({username}):**\n"
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
