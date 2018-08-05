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

import config
from scheduler import schedule_cron, exist_schedule, remove_schedule, list_schedules
from schedule_text_parser import parse_sch_text
from chat_tracking_db import create_table, add_chat, update_chat, get_elements


# API of the Currency Bot
TOKEN = config.BOT_TOKEN

# URL for accesing the API
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


# database
create_table()

# Variables
currency = None
user_location = {}
buy_or_sell = []


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


# For sending location from Bot API
# @param lat: latitude of the location
# @param lng: longitude of the location
# @param chat_id: ID for the receiver

def sendLocation(lat, lng, chat_id):

    url = URL + "sendlocation?chat_id={}&latitude={}&longitude={}".format(chat_id, lat, lng)

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


# Requests location of the user
# @param chat_id: chat id of the user

def requestLocation(chat_id):

    reply_markup = createKeyboard(["Send me your location"], location = True)

    sendMessage("Can you share your location with me?", chat_id, reply_markup)


# Updating process

def update(updates):

    for update in updates["result"]:

        chat = update["message"]["chat"]["id"]

        if "text" in update["message"]:

            text = update["message"]["text"]

            checkCommands(text, chat)

        elif "location" in update["message"]:

            location = update["message"]["location"]
            latitude = location["latitude"]
            longitude = location["longitude"]

            update_chat(chat, "location", "{}-{}".format(latitude, longitude))


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

    if currency:
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
    elif text == '/updateLocation':

        requestLocation(chat)

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
    elif text == '/listSchedules':

        sch_list = list_schedules(chat)

        if(len(sch_list) == 0):
            sendMessage("You have no schedules", chat)
        else:
            sch_markup = createKeyboard(sch_list)
            sendMessage("Select one to delete: ", chat, sch_markup)

    #-------------------------------------------------------------------------
    elif 'Remove schedule for' in text:

        removal = remove_schedule(text, chat)
        if removal:
            sendMessage("Schedule is removed successfully!", chat)

    #-------------------------------------------------------------------------
    elif re.match(r"[/]schedule(\s)?(\d+(\s)?day(s)?)?(\d+(\s)?hour(s)?)?(\d+(\s)?minutes(s)?)?(\d+(\s)?second(s)?)?", text):

        cmd_schedule_helper(currency, text, chat)

    #-------------------------------------------------------------------------
    else:
        if re.match(r"[/](\w)+", text):
            sendMessage("Unknown command '{}'".format(text), chat)
        else:
            update_chat(chat, "currency", text)
    #-------------------------------------------------------------------------

# Command best -- returns best rates according to the given currency
# @param currency: given currency
# @param buy_or_sell: will the currency be needed for buying or selling
# @param chat: chat ID

def cmd_best(currency, buy_or_sell, chat):

    if currency:
        from currency_scraping import fetchCurrency

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

    from currency_scraping import fetchCurrency

    buy_sell = None

    if text == buy_or_sell[0]:
        result = fetchCurrency(currency, 1)
        buy_sell = "(buy)"
    else:
        result = fetchCurrency(currency)
        buy_sell = "(sell)"

    if result:

        rate = result[0]
        bank_name = result[1]

        sendMessage("Best Choice for {} {} is {} in {}".format(currency, buy_sell, rate, bank_name), chat)

        # cmd_best_share_location(bank_name, chat)
    else:
        sendMessage("I could not find anything about {} :(".format(currency), chat)


# Shares the location of the bank with the given name
# @param bank_name: name of the bank
# @param chat: chat id

def cmd_best_share_location(bank_name, chat):

    location = get_elements("location", chat)[0]

    if location:
         user_location["lat"] = float(location.split("-")[0])
         user_location["lng"] = float(location.split("-")[1])

    if user_location:

        from location_scraping import findNearestBranchOfBank

        usr_lat = user_location["lat"]
        usr_lng = user_location["lng"]

        bank_name = re.sub(r"([a-z])([A-Z])", r"\1 \2", bank_name)

        result = findNearestBranchOfBank(usr_lat, usr_lng, bank_name)

        if result != None and  result != False:
            branch_geo = result["branch_geo_location"]
            branch_lat = branch_geo["lat"]
            branch_lng = branch_geo["lng"]

            sendMessage("Here is the location of '{}'".format(result["branch_name"]), chat)
            sendLocation(branch_lat, branch_lng, chat)
        else:
            sendMessage("Branch of '{}' is not found around you :(".format(bank_name), chat)
    else:
        sendMessage("Could not find your location :( If you want to share your location first just type '/updateLocation' then try your command again.", chat)


# Command nearest -- returns the nearest Bank centers
# @param currency: given currency
# @param chat: chat ID

def cmd_nearest(currency, chat):

    location = get_elements("location", chat)[0]

    if location:
         user_location["lat"] = float(location.split("-")[0])
         user_location["lng"] = float(location.split("-")[1])

    if user_location:
        from location_scraping import findNearestBranch

        usr_lat = user_location["lat"]
        usr_lng = user_location["lng"]

        result = findNearestBranch(usr_lat, usr_lng)

        if result:
            branch_name = result["branch_name"]
            branch_distance = result["branch_distance"]
            branch_geo_loc = result["branch_geo_location"]

            branch_lat = branch_geo_loc["lat"]
            branch_lng = branch_geo_loc["lng"]

            sendLocation(branch_lat, branch_lng, chat)
            sendMessage("Nearest bank branch around you is '{}'' and located {} kms away from you".format(branch_name, branch_distance), chat)
        else:
            sendMessage("Could not find any branches :(", chat)

    else:
        sendMessage("Could not find your location :( If you want to share your location first just type '/updateLocation' then try your command again.", chat)


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

    if currency ==  None:
        sendMessage("You have not sent me any currency yet", chat)
        return

    result = parse_sch_text(text)

    if exist_schedule(currency, chat):
        sendMessage("You have already set a schedule for {}.".format(currency), chat)
        sendMessage("You can view your schedules and remove them by '/listSchedules' command", chat)
    else:
        if schedule_cron(currency, chat, result) == True:
            sendMessage("Schedule is set!", chat)
        else:
            sendMessage("Something is wrong. Try again, please", chat)



# Updates the processes on foreground

def update_foreground():

    last_update_id = None

    while True:
        updates = getUpdates(last_update_id)

        if len(updates["result"]) > 0:
            last_update_id = getLastUpdateID(updates) + 1
            update(updates)

        time.sleep(1)

# Main function for executing all BOT functions
#
def main():

    update_foreground()


if __name__ == "__main__":

    main()
