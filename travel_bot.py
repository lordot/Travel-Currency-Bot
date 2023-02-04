import logging
import sys
import os

from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters

from sqlalchemy import exists

from models.database import DATABASE_NAME, Session, engine
from create_database import create_database
from models.currency import Currency
from models.chat import Chat

session = Session()

db_is_created = os.path.exists(DATABASE_NAME)
if not db_is_created:
    create_database()

CUR_BASE = session.query(Currency.name).all()
CUR_BASE.remove(('USD',))
USD = session.query(Currency.rate).filter(Currency.name == 'USD').scalar()

session.close()

TOKEN = os.getenv('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
APP_DOMAIN = os.getenv('APP_DOMAIN')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    level=logging.INFO,
)


def test(update, context):
    currencies = [cur for cur, in CUR_BASE]
    if update.message.text in currencies:
        session = Session()
        chat_id = update.effective_chat.id
        cur = session.query(Currency).filter(Currency.name == update.message.text).one()
        chat = session.query(Chat).filter(Chat.id == chat_id).one()
        chat.currency = cur
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Currency changed to *{cur.name}*, rate is *{cur.rate}* for *1$*',
            parse_mode='Markdown'
        )
        session.commit()
        session.close()


def change_currency(update, context):
    buttons = CUR_BASE
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Choose currency:',
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def get_rate(chat_id: int) -> float:
    session = Session()
    is_exists = session.query(exists().where(Chat.id == chat_id)).scalar()
    if not is_exists:
        default = session.query(Currency).first()
        new_chat = Chat(id=chat_id, currency_id=default.id)
        session.add(new_chat)
        session.commit()
        session.close()
    chat = session.query(Chat).filter(Chat.id == chat_id).one()
    return chat.currency.rate


def exchange(update, context):
    chat = update.effective_chat
    value = float(update.message.text)
    dollars = round(float(value / get_rate(chat.id)), 1)
    rubles = round(float(dollars * USD), 1)
    message = f'{dollars}$\n{rubles}₽'
    context.bot.send_message(
        chat_id=chat.id,
        text=message,
    )
    logging.info(f'{value} - {dollars} - {rubles}')


def main():
    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', change_currency))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$'), exchange))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, test))
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{APP_DOMAIN}/{TOKEN}"
    )
    updater.idle()


if __name__ == '__main__':
    main()
