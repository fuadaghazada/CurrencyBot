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
import re
import threading

from currency_scraping import fetchCurrency
from sch_timer import setTimer

from chat_tracking_db import create_table, add_chat, update_chat, get_elements
from location_scraping import findNearestBranch


# API of the Currency Bot
TOKEN = "576857231:AAHNRh1lacFO2ZZJ624ryJGuCmJ1AOB8FZs"

# URL for accesing the API
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


# database
create_table()

# Variables
currency = None
user_location = {}
buy_or_sell = []

# Timer
sch_state = None
sch_currency = None
sch_wait_time = None
sch_chat_id = None

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

def createKeyboard(items, location=False):

    keyboard = [[item] for item in items]

    if location ==  False:
        reply_markup = {"keyboard": keyboard, "one_time_keybaord": True}
    else:
        reply_markup = {"keyboard": [[{"text": "Share my location", "request_location" : True}]], "one_time_keybaord": True}

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

    for update in updates["result"]:

        if "text" in update["message"]:

            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]

            checkCommands(text, chat)

        elif "location" in update["message"]:

            location = update["message"]["location"]
            latitude = location["latitude"]
            longitude = location["longitude"]

            user_location["lat"] = latitude
            user_location["lng"] = longitude

            print(user_location)

# Checks the input messages/commands and reply according to them.
# Basicly, chat logic
# @param: text - content of the message
# @param: chat - chat of in which messaging occurs

def checkCommands(text, chat):

    global currency
    global buy_or_sell

    # Putting user requests in database
    add_chat(chat)
    currency = get_elements("currency", chat)[0]

    if currency != None:
        buy_or_sell = ["I want to buy {}".format(currency), "I want to sell {}".format(currency)]

    if text == '/start':

        sendMessage("Hello, I am Currency Bot. I will help you to get information about the currencies! You can type '/help' for learning what can I do for you!", chat)

    #-------------------------------------------------------------------------
    elif text == '/best':

        cmd_best(currency, buy_or_sell, chat)

    #-------------------------------------------------------------------------
    elif text in buy_or_sell:

        cmd_best_helper(currency, buy_or_sell, text, chat)

    #-------------------------------------------------------------------------
    elif text == '/nearest':

        cmd_nearest(currency, chat)

    #-------------------------------------------------------------------------
    elif text == '/list':

        cmd_list(chat)

    #-------------------------------------------------------------------------
    elif text == '/help':

        cmd_help(chat)

    #-------------------------------------------------------------------------
    elif text == '/schedule':

        cmd_schedule(currency, chat)

    #-------------------------------------------------------------------------
    elif re.match(r"[/]schedule(\s)?(\d+(\s)?day(s)?)?(\d+(\s)?hour(s)?)?(\d+(\s)?minutes(s)?)?(\d+(\s)?second(s)?)?", text):

        cmd_schedule_helper(currency, text, chat)

    #-------------------------------------------------------------------------
    else:
        if re.match(r"[/](\w)+", text):
            sendMessage("Unknown command '{}'".format(text), chat)
        else:
            #currency = text
            update_chat(chat, "currency", text)
    #-------------------------------------------------------------------------

# Command best -- returns best rates according to the given currency
# @param currency: given currency
# @param buy_or_sell: will the currency be needed for buying or selling
# @param chat: chat ID

def cmd_best(currency, buy_or_sell, chat):

    if currency:
        if  fetchCurrency(currency) or fetchCurrency(currency, 1):
            b_or_s_keyboard = createKeyboard(buy_or_sell)
            sendMessage("Select an option: ", chat, b_or_s_keyboard)
        else:
            sendMessage("I could not find anything about {} :(".format(currency), chat)
    else:
        sendMessage("You have not sent me any currency yet", chat)

# Command best (helper) -- returns best rates according to the given currency
# @param currency: given currency
# @param buy_or_sell: will the currency be needed for buying or selling
# @param text: User's input text
# @param chat: chat ID

def cmd_best_helper(currency, buy_or_sell, text, chat):

    if text == buy_or_sell[0]:
        result = fetchCurrency(currency, 1)
    else:
        result = fetchCurrency(currency)

    if result:

        rate = result[0]
        bank_name = result[1]

        sendMessage("Best Choice for {} is {} in {}".format(currency, rate, bank_name), chat)

    else:
        sendMessage("I could not find anything about {} :(".format(currency), chat)

# Command nearest -- returns the nearest Bank centers
# @param currency: given currency
# @param chat: chat ID

def cmd_nearest(currency, chat):

    reply_markup = createKeyboard(["Send me your location"], location = True)

    sendMessage("Can you share your location with me?", chat, reply_markup)

    if currency:
        if user_location:

            usr_lat = user_location["lat"]
            usr_lng = user_location["lng"]

            result = findNearestBranch(usr_lat, usr_lng)
            branch_name = result["branch_name"]
            branch_distance = result["branch_distance"]
            branch_geo_loc = result["branch_geo_location"]

            sendMessage("Nearest bank branch around you is {} and located {} km/s away from you".format(branch_name, branch_distance), chat)

        else:
            sendMessage("Could not find your location :(", chat)
    else:
        sendMessage("You have not sent me any currency yet", chat)

# Command list -- returns the list of commands
# @param chat: chat ID

def cmd_list(chat):

    result = "Here is the list of commands: \n\n"

    with open('list_of_commands.txt', 'r') as file:
        content = file.readlines()

    for line in content:
        command_name = line.split("##")[0]
        result += (command_name + "\n")

    sendMessage(result, chat)

# Command list -- returns the help message
# @param chat: chat ID

def cmd_help(chat):

    result = "Here is guide for using the commands: \n\n"

    with open('list_of_commands.txt', 'r') as file:
        content = file.readlines()

    for line in content:
        result += (line.replace('#', ' ') + "\n")

    sendMessage(result, chat)

# Command schedule -- returns the best rate after the given time
# @param currency: given currency
# @param chat: chat ID

def cmd_schedule(currency, chat):

    if currency:
        sendMessage("After how much do you want me to message you?\nHere is an example reply: /schedule 1 day 2 hours 1 minutes", chat)
    else:
        sendMessage("You have not sent me any currency yet", chat)

# Command schedule (helper) -- helps to parse the given time and set the timer
# @param currency: given currency
# @param text: User's input text
# @param chat: chat ID

def cmd_schedule_helper(currency, text, chat):

    global sch_state
    global sch_currency
    global sch_wait_time
    global sch_chat_id

    if currency ==  None:
        sendMessage("You have not sent me any currency yet", chat)
        return

    regex = re.compile("[/]schedule")
    resp = regex.sub("", text)

    numbers = re.findall(r"\d+", resp)
    time_names = re.findall(r"(day)[s]?|(hour)[s]?|(minute)[s]?|(second)[s]?", resp)

    days = 0
    hours = 0
    minutes = 0
    seconds = 0

    if len(numbers) != len(time_names):
        cmd_schedule(currency, chat)
        return
    else:
        for i in range(len(numbers)):

            for name in time_names[i]:
                if name != '':
                    if name == "day":
                        days = int(numbers[i])
                    elif name == "hour":
                        hours = int(numbers[i])
                    elif name == "minute":
                        minutes = int(numbers[i])
                    elif name == "second":
                        seconds = int(numbers[i])

    wait_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds

    # Due to 0.5 seconds delay on Telegram Updates
    #wait_seconds = wait_seconds * 2

    sendMessage("I will inform you about {} in {}. Just wait for me :)".format(currency, resp), chat)

    sch_wait_time = wait_seconds
    sch_currency = currency
    sch_chat_id = chat
    sch_state = True

    # TODO: Updating the database
    update_chat(chat, "schedule_state", sch_state)
    update_chat(chat, "schedule_currency", sch_currency)
    update_chat(chat, "schedule_wait_time", sch_wait_time)

# Updates processes on background
def update_background():

    num_of_users = len(get_elements("chat_id"))

    def update_timer(): #sch_chat_id, sch_state, sch_currency, sch_wait_time

        global sch_state
        global sch_currency
        global sch_wait_time
        global sch_chat_id

        while sch_state ==  None:
            if sch_state:
                break

        if sch_state:
            if setTimer(sch_wait_time) == True:

                buy_or_sell = ["I want to buy {}".format(sch_currency), "I want to sell {}".format(sch_currency)]
                cmd_best(sch_currency, buy_or_sell, sch_chat_id)
                sch_state = None

                update_chat(sch_chat_id, "schedule_state", None)
                update_chat(sch_chat_id, "schedule_currency", None)
                update_chat(sch_chat_id, "schedule_wait_time", None)

                update_background()

    update_timer()

    # for i in range(0, num_of_users):
    #     chat_id = get_elements("chat_id")[i]
    #     sch_state = get_elements("schedule_state", chat_id)[0]
    #     sch_currency = get_elements("schedule_currency", chat_id)[0]
    #        sch_wait_time = get_elements("schedule_wait_time", chat_id)[0]
    #
    #     if sch_state == "1":
    #         sch_wait_time = int(sch_wait_time)
    #         a_thread = threading.Thread(name='updateTimer', target=update_timer(chat_id, sch_state, sch_currency, sch_wait_time))
    #
    #         a_thread.start()
    #     else:
    #         continue


    #update_background()


# Updates the processes on foreground
def update_foreground():
    last_update_id = None

    while True:
        updates = getUpdates(last_update_id)

        if len(updates["result"]) > 0:
            last_update_id = getLastUpdateID(updates) + 1
            update(updates)

        time.sleep(0.5)

# Main function for executing all BOT functions
#
def main():

    foreground_thread = threading.Thread(name='foreground', target=update_foreground)
    background_thread = threading.Thread(name='background', target=update_background)

    background_thread.start()
    foreground_thread.start()


if __name__ == "__main__":

    main()
