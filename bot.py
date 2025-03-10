from telegram import ParseMode
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext

# 🔹 Твой токен от BotFather
TOKEN = "7965432987:AAFQqeT79_vO6YFh3s2hXTZxbJStLJ9HHe0"
# 🔹 ID канала, например "-1002468008518"
CHANNEL_ID = "-1002468008518"
# 🔹 Твой личный Telegram ID (узнать можно через @userinfobot)
ADMIN_ID = "752269181"


bot = Bot(token=TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Отправь мне анонимный вопрос, и я передам его автору.")

def handle_message(update: Update, context: CallbackContext):
    question = update.message.text

    # Отправляем вопрос автору (тебе)
    bot.send_message(chat_id=752269181, text=f"❓ Новый вопрос:\n{question}\n\nОтветь мне в ЛС, чтобы отправить ответ в канал!")

    # Отвечаем пользователю
    update.message.reply_text("Спасибо! Ваш вопрос передан.")

    # Сохраняем вопрос в контексте
    context.user_data['last_question'] = question

def handle_admin_reply(update: Update, context: CallbackContext):
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

    # Отправляем в канал
    bot.send_message(chat_id=-1002468008518, text=formatted_message, parse_mode=ParseMode.MARKDOWN)

    update.message.reply_text("Ответ отправлен в канал!")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
dp.add_handler(MessageHandler(Filters.text & Filters.chat(int(ADMIN_ID)), handle_admin_reply))

updater.start_polling()
updater.idle()
