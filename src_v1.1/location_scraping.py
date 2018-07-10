#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 11:04:04 2018

@author: fuadaghazada
"""

import requests
import math


def findNearestBranch(usr_loc, branch_addresses):

    distances = []

    for addr in branch_addresses:

        distance = findDistance(usr_loc = usr_loc, branch_loc = findBranch(addr))

        if distance:
            distances.append(distance)
        else:
            distances.append(math.inf)

    nearest_dist = min(distances)
    indexOFbranch = branch_addresses.index(nearest_dist)
    branch_address = branch_addresses[indexOFbranch]

    return {"name" : branch_address, "dist" : nearest_dist}


def findDistance(usr_loc, branch_loc):

    if branch_loc:
        lat2 = branch_loc["lat"]
        lng2 = branch_loc["lng"]

        lat1 = branch_loc["lat"]
        lng1 = branch_loc["lng"]

        distance = calculateDistantceKM(lat1, lng1, lat2, lng2)

        return distance
    else:
        return None


def findBranch(branch_address):

    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=false'.format(branch_address))

    resp_json_payload = response.json()

    results = resp_json_payload['results']

    if len(results) == 0:
        return None
    else:
        return results[0]['geometry']['location']


def findBanksNearby(usr_lat, usr_lng):

    loc = "location={},{}".format(usr_lat, usr_lng)
    rad = "&radius={}".format(5000)
    type = "&types=restaurant"
    sensor = "&sensor=true"
    key = "&key=AIzaSyDC4ketwopWVFq9LKrvAcCPcCBrKJewDj4"

    response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?{}{}{}{}{}".format(loc, rad, type, sensor, key))

    resp_json_payload = response.json()

    results = resp_json_payload['results']

    for result in results:
        print(result['geometry']['location'])
        print(result['formatted_address'])


def calculateDistantceKM(latitude1, longitude1, latitude2, longitude2):

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




my_location = {"lat" : 40.3880373, "lng" : 49.8263347}

#print(findBank("Yasamal rayounu, Xidir Mustafayev"))
#findBanksNearby(usr_lat = 40.3880373, usr_lng = 49.8263347)
#findBanksNearby(usr_lat = 37.77657, usr_lng = -122.417506)
#print(findBank("Bakı şəh., Şərifzadə küç. 75A"))

#print(findDistance(usr_loc = my_location, bank_loc = findBranch("Bakı şəh., Neftçilər pr. 67")))

list_of_br_addrs = ["Bakı şəh., Alı Mustafayev küç., 1c, AZ 1111",
                    "Bakı şəh., Azadlıq pr., 97, AZ 1000",
                    "Bakı şəh., Babek pr. 76c, AZ 1030",
                    "Bakı şəh., Badamdar qəsəbəsi, 1-ci Yaşayış Massivi, Badamdar şossesi, ev 34, AZ1023",
                    "Bakı şəh., M. Fətəliyev küc. 70, AZ 1132",
                    "Bakı şəh., Əlövsət Quliyev küç., 137, AZ 1000",
                    "Bakı şəh., Şövkət Məmmədova küç. 91, AZ1000",
                    "Bakı şəh., Bül-Bül pr. 33, AZ 1022",
                    "Bərdə şəh., İsmət Qayıbov küç., 8A, AZ0900",
                    "Cəlilabad şəh., H.Əliyev pr., 4, AZ1500",
                    "Bakı şəh., Inşaatçılar pr., 4a, AZ 1073",
                    "Göyçay şəh., H.Əliyev prospekti 96, AZ2300",
                    "Gəncə şəh. M.A.Abbaszadə küç. 32, AZ2000"
]

print(findNearestBranch(usr_loc = my_location, branch_addresses = list_of_br_addrs))
