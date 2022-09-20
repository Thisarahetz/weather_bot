from telegram.ext import Updater, CommandHandler, ContextTypes, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from weather import get_forecasts
import os
from dotenv import load_dotenv

# get token from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

# check for new masg
updater = Updater(TOKEN)

# allow the register handler (text,Image,video)
dispatcher = updater.dispatcher


# define a command callback function
def start(update, context):
    context.bot.sendMessage(chat_id=update.message.chat_id, text="Hello, Welcome to WeatherXYZ....\nEnter your Name:-")


# crate command handler
start_handler = CommandHandler("start", start)

updater.dispatcher.add_handler(start_handler)


# add command handler to dispatcher
# dispatcher.add_handler(start_handler)


# masg handler
def echo(update, context):
    context.bot.sendMessage(chat_id=update.message.chat_id, text="Hello.." + update.message.text)


# Create text handler
echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)
updater.dispatcher.add_handler(echo_handler)


def option(update, context):
    button = [
        [InlineKeyboardButton("Check weather", callback_data="1"),
         InlineKeyboardButton("Option 2", callback_data="2")],
        [InlineKeyboardButton("Option 3", callback_data="3")]
    ]
    reply_markup = InlineKeyboardMarkup(button)
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text="Chose one option...",
                            reply_markup=reply_markup)


def button_click(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  text="Thanks for choosing {}.".format(query.data),
                                  message_id=query.message.message_id)


button_handler = CallbackQueryHandler(button_click)
updater.dispatcher.add_handler(button_handler)

# create command /option
option_handler = CommandHandler("option", option)
updater.dispatcher.add_handler(option_handler)


def location(update, context):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    forecast = get_forecasts(lat, lon)
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=forecast,
                            reply_markup=ReplyKeyboardRemove())


def get_location(update, context):
    button = [
        [KeyboardButton("Share Location", request_location=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(button)
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text="Mind Share Location...",
                            reply_markup=reply_markup)


get_location_handler = CommandHandler("weather", get_location)
updater.dispatcher.add_handler(get_location_handler)


location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)

# start polling
updater.start_polling()
