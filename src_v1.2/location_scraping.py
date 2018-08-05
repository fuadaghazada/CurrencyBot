#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 11:04:04 2018

@author: fuadaghazada
"""


import math
import time
from googleplaces import GooglePlaces, types, lang

import config

# Google Map API key
API_KEY = config.API_KEY


# Calculates distance between two lat-s and two long-s in KM using Haversine formula
# @return d: distance in KM
#
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

# Finds nearby places to the given latitude and longitude in the given radius
# @param usr_lat: Latitude of the user
# @param usr_lng: Longitude of teh user
# @param radius: given radius

def findNearbyBranches(usr_lat, usr_lng, search_radius):

    if usr_lat == None or usr_lng ==  None:
        return None

    try:
        branches = []

        google_places = GooglePlaces(API_KEY)

        query_result = google_places.nearby_search(
                lat_lng = {'lat': usr_lat, 'lng': usr_lng},
                keyword = 'Banks',
                radius = search_radius,
                types = [types.TYPE_BANK])

        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:

            branch_name = place.name

            branch_geo_loc = place.geo_location
            branch_lat = float(branch_geo_loc["lat"])
            branch_lng = float(branch_geo_loc["lng"])

            distance = calculateDistantceKM(usr_lat, usr_lng, branch_lat, branch_lng)
            distance = math.ceil(distance * 1000) / 1000

            # Putting result in a list of tuples
            result = (branch_name, branch_geo_loc, distance)

            branches.append(result)

    except Exception as e:
        print(str(e) + str("findNearbyBranches"))
        return None

    # Returing the list of branches in given radius
    return branches


# Finds the nearest branch of the given bank
# @param usr_lat: latitude of the user
# @param usr_lng: longitude of the user
# @param bank_name: name of the given bank

def findNearestBranchOfBank(usr_lat, usr_lng, bank_name):

    if usr_lat == None or usr_lng ==  None:
        return None

    try:
        print("point1")

        google_places = GooglePlaces(API_KEY)

        print("point2")

        # List of autocompletion of Google Maps
        predictions = google_places.autocomplete(input = str(bank_name), lat_lng = {'lat': usr_lat, 'lng': usr_lng})._predictions

        branch_names = []
        branch_geo_locs = []
        distances = []

        print("point3")

        for prediction in predictions:

            print("point4")

            place = google_places.get_place(prediction._place_id)
            branch_names.append(place._name)
            branch_geo_locs.append(place._geo_location)

            if "ATM" in place._name:
                distances.append(math.inf)
            else:
                distance = calculateDistantceKM(usr_lat, usr_lng, float(place._geo_location["lat"]), float(place._geo_location["lng"]))
                distances.append(distance)

        if len(branch_names) == 0:
            print("No result is found")
            return None
        else:
            nearest_distance = min(distances)
            index_of_nearest = distances.index(nearest_distance)
            nearest_branch_name = branch_names[index_of_nearest]
            nearest_branch_geo_loc = branch_geo_locs[index_of_nearest]

            return {"branch_name" : nearest_branch_name, "branch_distance" : nearest_distance, "branch_geo_location" : nearest_branch_geo_loc}

    except Exception as e:
        print(str(e) + str("findNearestBranchOfBank"))
        return None

# Finds the nearest branch according to the given radius and location
# @param usr_lat: Latitude of the user location
# @param usr_lng: Longitude of the user location
# @param radius: Raduis of of search

def findNearestBranch(usr_lat, usr_lng, radius = 1000):

    branches = findNearbyBranches(usr_lat, usr_lng, radius)

    if branches == None:
        return None

    branch_names = []
    branch_geo_locs = []
    distances = []

    for branch in branches:
        branch_names.append(branch[0])
        branch_geo_locs.append(branch[1])
        distances.append(branch[2])

    if len(distances) == 0:
        return findNearestBranch(usr_lat, usr_lng, radius + 1000)

    elif len(distances) == 0 and radius >= 5000:
        print("No bank branch is found in radius of 10 km")
        return False
    else:
        nearest_distance = min(distances)
        index_of_nearest = distances.index(nearest_distance)
        nearest_branch_name = branch_names[index_of_nearest]
        nearest_branch_geo_loc = branch_geo_locs[index_of_nearest]

        return {"branch_name" : nearest_branch_name, "branch_distance" : nearest_distance, "branch_geo_location" : nearest_branch_geo_loc}


#print(findNearestBranch(40.397922, 49.800599, "ASB"))
#print(findNearestBranch(40.397922, 49.800599))
#print(findNearestBranchOfBank(40.397922, 49.800599, "Bank of Baku"))
