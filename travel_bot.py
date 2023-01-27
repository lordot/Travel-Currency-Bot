import os
import logging
import sys

from telegram.ext import Updater, MessageHandler, Filters

TOKEN = '5542961975:AAHHVziYdOyIU5giQmNEBGm4JYY0idksn1Y'
PORT = '5000'
# CERT = os.getenv('CERT')
APP_DOMAIN = 'travel-bot.104.198.156.86.sslip.io'
IDRDOL = '123'
DOLRUB = '123'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    level=logging.INFO,
)


def exchange(update, context):
    chat = update.effective_chat
    value = float(update.message.text)
    dollars = round(float(value/IDRDOL), 1)
    rubles = round(float(dollars*DOLRUB), 1)
    message = f'{dollars}$\n{rubles}₽'
    context.bot.send_message(
        chat_id=chat.id,
        text=message,
    )
    logging.info(f'{value} - {dollars} - {rubles}')


def main():
    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$'), exchange))
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{APP_DOMAIN}/{TOKEN}",
        # cert=CERT
    )
    updater.idle()


if __name__ == '__main__':
    main()
