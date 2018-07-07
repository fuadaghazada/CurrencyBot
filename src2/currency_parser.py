#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 18:44:44 2018

@author: fuadaghazada
"""

import json
import requests
import datetime
from collections import OrderedDict


# URL of azn.today for getting the currency information
URL = "http://azn.today/api/banks"

# Sends request to the given URL (API) and accesses the JSON content
# 
# @return JSON content
def fetchAPI():
    
    content = requests.get(URL).content.decode("utf8")
    
    return json.loads(content)

# Fetches the given currency with the best rate
#
#
def fetchCurrency(currency, buyORsell = 0):
    
    if buyORsell == 0:
        buyORsell = "buy"
    else:
        buyORsell = "sell"
       
    json_content = fetchAPI()[getCurrentDate()]
    data = OrderedDict(json_content)
    
    # Getting banks from the json        
    bank_names = list(data.keys())
    
    # all rates of the given currency
    rates = []
    
    for i in range(0, len(bank_names)):
        
        bank = bank_names[i]
        currencies = json_content[bank][buyORsell]
        
        for cur in currencies:
            if cur["name"] == currency:
                rates.append(float(cur["value"]))
    
    result_bank_names = []
    
    for rate in rates:
        if rate == min(rates):
            i = rates.index(rate)
            result_bank_names.append(bank_names[i])
            
    result_bank_names = set(result_bank_names)
            
    return (min(rates), result_bank_names)
    
    

# Gets the current date from the system and returns it as string
#    
# @return DD.MM.YY
def getCurrentDate():
    
    current_date = str(datetime.datetime.now()).split(" ")[0].split("-")
    
    day = current_date[2]
    month = current_date[1]
    year = current_date[0]
    
    date_str = str("{}.{}.{}".format(day, month, year))
    
    return date_str



fetchCurrency("usd", 1)


