import logging
import sys
import os

from telegram.ext import Updater, MessageHandler, Filters

from models.database import DATABASE_NAME
from create_database import create_database

TOKEN = '5542961975:AAHHVziYdOyIU5giQmNEBGm4JYY0idksn1Y'
IDRDOL = 14.975
DOLRUB = 62.5

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
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_database()
    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$'), exchange))
    updater.start_polling(2)
    updater.idle()


if __name__ == '__main__':
    main()
