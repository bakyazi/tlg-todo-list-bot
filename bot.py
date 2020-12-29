import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import pymongo
import emoji

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = 'YOUR-TELEGRAM-BOT-TOKEN'
HEROKU_APP_URL = 'HEROKU-APP-URL'
PORT = int(os.environ.get('PORT', 5000))


MONGODB_CLIENT = 'MONGODB-CONNECTION-URL'
DB_NAME = 'DB-NAME'
COLLECTION_NAME = 'COLLECTION-NAME'


client = pymongo.MongoClient(MONGODB_CLIENT)
db = client[DB_NAME]
todo_list = db[COLLECTION_NAME]

def start(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update["message"]["chat"]["id"]
    todo_list.find_one_and_update({'chat_id' : chat_id}, {"$set": {"todo_list": []}}, upsert=True)
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def to_do(update, context):
    chat_id = update["message"]["chat"]["id"]
    text = " ".join(update["message"]["text"].split(' ')[1:])
    todo_list.find_one_and_update({'chat_id' : chat_id}, {"$push": {"todo_list": text}})
    update.message.reply_text("Added!")

def list_items(update, context):
    chat_id = update["message"]["chat"]["id"]
    _list = todo_list.find_one({'chat_id' : chat_id})
    text = ""
    for index, item in enumerate(_list["todo_list"]):
        text += str(index + 1) + "- " + item + "\n"
    update.message.reply_text(text)

def done(update, context):
    try:
        chat_id = update["message"]["chat"]["id"]
        text = " ".join(update["message"]["text"].split(' ')[1:])
        index = int(text)
        index -= 1

        parrent_item = todo_list.find_one({"chat_id": chat_id}, {"todo_list" : 1})
        item = parrent_item["todo_list"][index]

        todo_list.update({"chat_id": chat_id},  {"$push": {"done_list": item}})
        todo_list.update({"chat_id" : chat_id}, {"$unset": {"todo_list." + str(index) : 1}})
        todo_list.update({"chat_id" : chat_id}, {"$pull": {"todo_list" : None}})        
        update.message.reply_text("Done!")
    except:
        update.message.reply_text("Failed!")

def get_done_list(update, context):
    try:    
        chat_id = update["message"]["chat"]["id"]
        _list = todo_list.find_one({'chat_id' : chat_id})
        text = ""
        for index, item in enumerate(_list["done_list"]):
            text += emoji.emojize(':white_check_mark:', use_aliases=True) + " " + item + "\n"
        update.message.reply_text(text)
    except:
        update.message.reply_text("Failed!")

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("todo", to_do))
    dp.add_handler(CommandHandler("done", done))
    dp.add_handler(CommandHandler("dones", get_done_list))
    dp.add_handler(CommandHandler("list", list_items))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(HEROKU_APP_URL + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()