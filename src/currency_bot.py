#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 10:56:06 2018

@author: fuadaghazada
"""
import json
import requests
import time
import urllib
import telegram
from enum import Enum
from schedule import Scheduler

# API of the Currency Bot
TOKEN = "BOT API"

# URL for accesing the API
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# Currency
currency = None
user_location = (None, None)

scheduler = None

last_chat_id = None

class Schedule_State(Enum):

    NO_SCHEDULE = 0
    WAITING_FOR_DATE = 1
    GOING_ON = 2
    FINISHED = 3

schedule_state = Schedule_State.NO_SCHEDULE

# Access the URL and catch the content of the URL in UTF-8
# @param: url - given url
# @return: content - content of the url

def getURL(url):
    response = requests.get(url)
    content = response.content.decode("utf8")

    return content

# Loads the content of the given url in JSON format
# @param: url - given url
# @return: js - content in JSON format

def getJSON(url):
    content = getURL(url)
    js = json.loads(content)

    return js

# Acesses the updates in the API according to the given offset
# @param: (default None) - given offset
# @return: js - updates in JSON format

def getUpdates(offset = None):
    url = URL + "getUpdates?timeout=100"

    if offset:
        url += "&offset={}".format(offset)
    js = getJSON(url)

    return js

# For sending Message from Bot API
# @param: text - content of message
# @param: chat_id - ID for the receiver chat
# @param: reply_markup - for creating custom keyboard

def sendMessage(text, chat_id, reply_markup = None):
    text = urllib.parse.quote_plus(text)    # for parsing special chars like + - & etc.

    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)

    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)

    getURL(url)

# Creates a custom keyboard with the given items
# @param: items - keyboard items
# @return reply_markup_

def createKeyboard(items):
    keyboard = [[item] for item in items]

    reply_markup = {"keyboard": keyboard, "one_time_keybaord": True}

    return json.dumps(reply_markup)

# Returns the latest update ID
# @param: updates - all the updates
# @return: max of the update ids

def getLastUpdateID(updates):
    update_ids = []

    for update in updates["result"]:

        update_ids.append(int(update["update_id"]))

    return max(update_ids)

# Updating process

def update(updates):

    global last_chat_id

    for update in updates["result"]:

        if "text" in update["message"]:

            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]

            last_chat_id = chat

            checkCommands(text, chat)

        elif "location" in update["message"]:

            location = update["message"]["location"]
            latitude = location["latitude"]
            longitude = location["longitude"]

            user_location = (latitude, longitude)
            print(user_location)

# Checks the input messages/commands and reply according to them.
# Basicly, chat logic
# @param: text - content of the message
# @param: chat - chat of in which messaging occurs

def checkCommands(text, chat):

    global currency
    global schedule_state
    global scheduler

    if text == '/start':

        sendMessage("Hello, I am Currency Bot. I will help you to get information about the currencies! You can type '/help' for learning what can I do for you!", chat)

    #-------------------------------------------------------------------------
    elif text == '/best':

        if currency:
            sendMessage("Best Choice for {} is {}".format(currency, -1), chat)
        else:
            sendMessage("You have not sent me any currency yet", chat)
    #-------------------------------------------------------------------------
    elif text == '/nearest':

        location_keyboard = telegram.KeyboardButton(text="Send Location", request_location=True)
        custom_keyboard = [[location_keyboard]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

        sendMessage("Can you share your location with me?", chat, reply_markup)

        if currency:
            sendMessage("Nearest ATM for {} is in {}".format(currency, -1), chat)
        else:
            sendMessage("You have not sent me any currency yet", chat)
    #-------------------------------------------------------------------------
    elif text == '/list':

        result = "Here is the list of commands: \n\n"

        with open('list_of_commands.txt', 'r') as file:
            content = file.readlines()

        for line in content:
            command_name = line.split("##")[0]
            result += (command_name + "\n")

        sendMessage(result, chat)
    #-------------------------------------------------------------------------
    elif text == '/help':

        result = "Here is guide for using the commands: \n\n"

        with open('list_of_commands.txt', 'r') as file:
            content = file.readlines()

        for line in content:
            result += (line.replace('#', ' ') + "\n")

        sendMessage(result, chat)
    #-------------------------------------------------------------------------
    elif text == '/schedule':

        if currency:
            schedule_state = Schedule_State.WAITING_FOR_DATE

            sendMessage("Enter a date in format dd/mm/YY/HH:MM", chat)
        else:
            sendMessage("You have not sent me any currency yet", chat)
    #-------------------------------------------------------------------------
    elif schedule_state == Schedule_State.WAITING_FOR_DATE:

        parts = text.split("/")

        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])
        hours = int(parts[3].split(":")[0])
        minutes = int(parts[3].split(":")[1])

        scheduler = Scheduler(day, month, year, hours, minutes)

        sendMessage("Date is scheduled for {}/{}/{} in {}:{}".format(day, month, year, hours, minutes), chat)

        scheduler.start()

        schedule_state = Schedule_State.GOING_ON

    #-------------------------------------------------------------------------
    else:
        if len(text.split("/")) == 1 and len(text.split(":")) == 1:
            currency = text
    #-------------------------------------------------------------------------

def updateScheduler():

    global scheduler

    if scheduler != None:

        print("Initialized")

        if scheduler.hasTimeArrived() ==  True:

            sendMessage("Done!", last_chat_id)

            scheduler = None

            print("Finished")
    else:
        print("None")

def main():

    last_update_id = None

    while True:
        updates = getUpdates(last_update_id)

        if len(updates["result"]) > 0:
            last_update_id = getLastUpdateID(updates) + 1
            update(updates)

        updateScheduler()

        time.sleep(0.5)


if __name__ == "__main__":
    main()
