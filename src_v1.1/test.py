#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 16:47:35 2018

@author: fuadaghazada
"""

from googleplaces import GooglePlaces, types, lang

API_KEY = 'AIzaSyDC4ketwopWVFq9LKrvAcCPcCBrKJewDj4'

google_places = GooglePlaces(API_KEY)

query_result = google_places.nearby_search(
    lat_lng={'lat': 40.3737746, 'lng': 49.8292541},
    radius=1000, types=[types.TYPE_BANK])

if query_result.has_attributions:
    print (query_result.html_attributions)

for place in query_result.places:
    place.get_details()
    print (place.rating)
