import os
import logging
import sys

from telegram.ext import Updater, MessageHandler, Filters

TOKEN = os.getenv('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
APP_NAME = os.getenv('APP_NAME')
IDRDOL = float(os.getenv('IDRDOL'))
IDRRUB = float(os.getenv('IDRRUB'))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    level=logging.INFO,
)


def exchange(update, context):
    chat = update.effective_chat
    value = float(update.message.text)
    dollars = round(float(value/IDRDOL), 1)
    rubles = round(float(dollars*IDRRUB), 1)
    message = f'{dollars}$\n{rubles}₽'
    context.bot.send_message(
        chat_id=chat.id,
        text=message,
    )
    logging.info(f'{value} - {message}')


def main():
    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$'), exchange))
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{APP_NAME}.herokuapp.com/{TOKEN}"
    )
    updater.idle()


if __name__ == '__main__':
    main()
