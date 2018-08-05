#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 10:53:04 2018

@author: fuadaghazada
"""

import math
import requests
import re
from bs4 import BeautifulSoup

# URL of the 'azn.today'
URL = "https://azn.today/"


# Fetches the html content of the given URL
def fetchPageContent(url):

    try:
        content = requests.get(URL).content

        return content
    except:
        return None


# Fetches the page and parsing though the currency table
def fetchTableInformation():

    page = fetchPageContent(URL)

    if page == None:
        return None

    soup = BeautifulSoup(page, 'html.parser')

    try:
        # Table of currency
        currency_table = soup.find_all("table")[1]

        headers = []
        for head in currency_table.find_all("th"):
            headers.append(head.text)

        currency_table = currency_table.tbody

        # Rows
        rows = currency_table.find_all("tr")

        row_info = []
        bank_names = []

        for row in rows:
            row = row.text

            row = replaceAZletters(row)

            regex = re.compile(r"([-+]?\d*(\.\d+|\d+))?(%)")
            line = regex.sub(" ", row)

            regex = re.compile(r"(---)")                    # TODO: Put it into a 'smart' way
            line = regex.sub("999", line)                   # TODO: Put it into a 'smart' way

            regex = re.compile(r"(\s)+")
            line = regex.sub("#", line)

            bank_name = re.match(r"(#)[a-zA-Z(# | \-)?]+", line).group()

            regex = re.compile(r"\-")
            bank_name = regex.sub("", bank_name)

            regex = re.compile(r"#")
            bank_name = regex.sub("", bank_name)

            regex = re.compile(r"(#)[^0-9]+(#)")            # TODO: Put it into a 'smart' way
            line = regex.sub("", line)

            # Adding
            row_info.append(line)
            bank_names.append(bank_name)

        return (headers, bank_names, row_info)

    except Exception as e:
        print(e)
        return None

# Fetches the needed currency from the
def fetchCurrency(currency, buyORsell = 0):

    if fetchTableInformation() ==  None:
        return None

    table_information = fetchTableInformation()

    headers = table_information[0]
    bank_names = table_information[1]
    row_info = table_information[2]

    # Checking whether the buy or sell is claimed
    if buyORsell == 0:
        buyORsell = "buy"
    else:
        buyORsell = "sell"

    currency = str(currency).lower()

    # Index for needed currency and buy/sell
    curr_index = -1

    for header in headers:
        header_low = str(header).lower()

        if (currency in header_low) and (buyORsell in header_low):
            curr_index = headers.index(header)

    # In case user typed wrong or / no currency is in the table
    if curr_index == -1:
        print("No such a currency is found!")
        return None

    rates = []

    for row in row_info:
        curr_row = str(row).split("#")
        rate = float(curr_row[curr_index - 1])

        if rate == 999:                                     #TODO: Again 'SMART'
            rates.append(math.inf)
        else:
            rates.append(rate)

    ## RESULTS
    if len(rates) == 0:
        return None

    if buyORsell == "sell":
        result_rate = min([n for n in rates  if n > 0])
    else:
        result_rate = max([n for n in rates  if n < math.inf])

    index_rate = rates.index(result_rate)
    bank = bank_names[index_rate]

    return (result_rate, bank)



def replaceAZletters(word):

    regex = re.compile("(ə)")
    line = regex.sub("e", word)

    regex = re.compile("(ı)")
    line = regex.sub("i", line)

    regex = re.compile("(Ə)")
    line = regex.sub("E", line)

    regex = re.compile("(I)")
    line = regex.sub("İ", line)

    regex = re.compile("(Ş)")
    line = regex.sub("Sh", line)

    regex = re.compile("(ş)")
    line = regex.sub("sh", line)

    regex = re.compile("(Ç)")
    line = regex.sub("Ch", line)

    regex = re.compile("(ç)")
    line = regex.sub("ch", line)

    regex = re.compile("(Ğ)")
    line = regex.sub("G", line)

    regex = re.compile("(ğ)")
    line = regex.sub("g", line)

    regex = re.compile("(Ö)")
    line = regex.sub("O", line)

    regex = re.compile("(ö)")
    line = regex.sub("o", line)

    regex = re.compile("(Ü)")
    line = regex.sub("U", line)

    regex = re.compile("(ü)")
    line = regex.sub("u", line)

    return line
