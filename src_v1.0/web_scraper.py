#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 21:19:30 2018

@author: fuadaghazada
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import math


class BankDataScraper:

    def fetchBankRates(self, index):
        # Will be implemented
        pass

    def fetchBankInformation(self, index):

        banks = self.fetchBanks()

        if index < len(banks):

            bank = banks[index]

            bank_name = bank[0]
            bank_href = bank[1]

            page = urlopen("http://banks.az/" + bank_href)

            soup = BeautifulSoup(page, 'html.parser')

            bank_site = soup.find('div', attrs = {'id':'che888'})

            if bank_site ==  None:

                print("No atm")

                return dict({"name":bank_name, "website":bank_site, "atms":None})

            else:

                list_of_atms_html = bank_site.findAll('a')

                list_of_atms = []

                for atm in list_of_atms_html:

                    location_param = atm.get('href')
                    location_address = atm.get_text()

                    # Extracting longitude and latitude from 'location_param'
                    lat_long_id = location_param.split("?")[1]
                    lat = lat_long_id.split("&")[0]
                    long = lat_long_id.split("&")[1]

                    latitude = re.search(r'([0-9]*\.)?[0-9]+', lat).group()
                    longitude = re.search(r'([0-9]*\.)?[0-9]+', long).group()

                    list_of_atms.append((latitude, longitude, location_address))

            return dict({"name":bank_name, "website":bank_site, "atms":list_of_atms})

        else:
             print("Index Out of Bounds")


    def fetchBankName(self, index):

        return self.fetchBankInformation(index)["name"]


    def fetchBankWebsite(self, index):

        return self.fetchBankInformation(index)["website"]


    def fetchBankATMs(self, index):

        return self.fetchBankInformation(index)["atms"]

    def fetchATM(self, bank_index, atm_index):

        if self.fetchBankATMs(bank_index) ==  None:
            return dict({"latitude" : self.fetchBankATMs(bank_index)[atm_index][0], "longitude" : self.fetchBankATMs(bank_index)[atm_index][0]})
        else:
            return None

    # Not implemented YET
    def fetchNearATM(self, latitude, longitude):

        banks = self.fetchBanks()

        for i in range(0, len(banks)):

            if self.fetchBankATMs(i) !=  None:

                atms = self.fetchBankATMs(i)

                for j in range(0, len(atms)):

                    print(atms[j])
                    #print(atm)


    def calculateDistantceKM(self, latitude1, longitude1, latitude2, longitude2):

        """
        Haversine formula:	a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
                            c = 2 ⋅ atan2( √a, √(1−a) )
                            d = R ⋅ c

            where	φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
            note that angles need to be in radians to pass to trig functions!

            reference: http://www.movable-type.co.uk/scripts/latlong.html
        """
        # Radius of Earth in km' s
        EARTH_RADIUS = 6371

        # Calculating distances to all ATMs (for now it is in O(n x m) efficiency, it would be improved)
        d_latitude = (latitude2 - latitude1) * (math.pi / 180)
        d_longitude = (longitude2 - longitude1) * (math.pi / 180)

        a = math.sin(d_latitude/2) * math.sin(d_latitude/2) + math.cos(latitude1 * (math.pi / 180)) * math.cos(latitude2 * (math.pi / 180)) * math.sin(d_longitude/2) * math.sin(d_longitude/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = EARTH_RADIUS * c

        return d


    def fetchBanks(self):

        data = []

        # URL of 'banks.az'
        page_url =  "http://banks.az/banks.php?lang=az"

        # HTML content of the url
        page = urlopen(page_url)

        # Soup object for parsing
        soup = BeautifulSoup(page, 'html.parser')

        list_of_banks = soup.find_all('a', attrs = {'class':'newshead'})

        for bank in list_of_banks:

            name_of_bank = bank.get_text()

            href_of_bank = bank.get('href')

            data.append((name_of_bank, href_of_bank))

        return data
    

bankScrp = BankDataScraper()

#for i  in bankScrp.fetchBankATMs(0):
#    print(str(i[0]) + "\t" + str(i[1]) + "\n")

#print(bankScrp.calculateDistantceKM(40.397951, 49.800645, 40.613952, 49.670334))

print(bankScrp.fetchNearATM(40.397951, 49.800645))

#bankScrp.storeToDb()
