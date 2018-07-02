
import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

from schedule import Scheduler

# API of the @currency_tracket_bot
updater = Updater(token='576857231:AAHNRh1lacFO2ZZJ624ryJGuCmJ1AOB8FZs')

# dispatcher for handling the Handlers
dispatcher = updater.dispatcher

# current currency requested
recent_currency_accessed = None

scheduler = None

#------------------------------------------------------------------------------------------------------------

def cmd_best(bot, update):

	if recent_currency_accessed == None:
		bot.send_message(chat_id=update.message.chat_id, text="You have not sent me any currency yet")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Not implemented yet")

best_handler = CommandHandler("best", cmd_best)

dispatcher.add_handler(best_handler)

#------------------------------------------------------------------------------------------------------------

def cmd_nearest(bot, update):

	location_keyboard = telegram.KeyboardButton(text="Send Location", request_location=True)
	custom_keyboard = [[location_keyboard]]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

	bot.send_message(chat_id=update.message.chat_id, text="Can share your location with me?", reply_markup=reply_markup)

	print(dispatcher.update_queue.peek())

	if recent_currency_accessed == None:
		bot.send_message(chat_id=update.message.chat_id, text="You have not sent me any currency yet")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Not implemented yet")

	#bot.sendLocation(chat_id=update.message.chat_id, latitude=49.9, longitude=49.9)

location_handler = CommandHandler('nearest', cmd_nearest)

dispatcher.add_handler(location_handler)

#------------------------------------------------------------------------------------------------------------

def cmd_start(bot, update):

	bot.send_message(chat_id=update.message.chat_id, text="Hello, I am Currency Bot. I will help you to get information about the currencies! You can type '/help' for learning what can I do for you!")

start_handler = CommandHandler("start", cmd_start)

dispatcher.add_handler(start_handler)

#------------------------------------------------------------------------------------------------------------

def cmd_list(bot, update):

	result = "Here is the list of commands: \n\n"

	with open('list_of_commands.txt', 'r') as file:
		content = file.readlines()

	for l in content:
		command_name = l.split("##")[0]
		result += (command_name + "\n")

	bot.send_message(chat_id=update.message.chat_id, text=result)

list_handler = CommandHandler("list", cmd_list)

dispatcher.add_handler(list_handler)

#------------------------------------------------------------------------------------------------------------

def cmd_help(bot, update):

	result = "Here is guide for using the commands: \n\n"

	with open('list_of_commands.txt', 'r') as file:
		content = file.readlines()

	for l in content:
	    result += (l.replace('#', ' ') + "\n")

	bot.send_message(chat_id=update.message.chat_id, text=result)

help_handler = CommandHandler("help", cmd_help)

dispatcher.add_handler(help_handler)

#------------------------------------------------------------------------------------------------------------

def cmd_schedule(bot, update):

	if recent_currency_accessed == None:
		bot.send_message(chat_id=update.message.chat_id, text="You have not sent me any currency yet")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Please, enter a data and time for the schedule (in format dd/mm/YY/HH:MM)")


schedule_handler = CommandHandler("schedule", cmd_schedule)

dispatcher.add_handler(schedule_handler)

#------------------------------------------------------------------------------------------------------------

def currency_sent(bot, update):

	global recent_currency_accessed

	text = update.message.text

	recent_currency_accessed = text

currency_handler = MessageHandler(Filters.text, currency_sent)

dispatcher.add_handler(currency_handler)

#------------------------------------------------------------------------------------------------------------

updater.start_polling()
