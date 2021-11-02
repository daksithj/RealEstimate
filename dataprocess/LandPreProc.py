from django.db import models
from django.utils import timezone
from webscrape.models import RawLandData
from django.shortcuts import render, redirect
from .models import ProcLandData
import re
import requests
import datetime
from googlegeocoder import GoogleGeocoder


# api key : AIzaSyC4pgdGcQIgG4_Pf6I4hlYq2GrygqaAFgo
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
GOOGLE_MAPS_API_KEY =  'AIzaSyC4pgdGcQIgG4_Pf6I4hlYq2GrygqaAFgo'
NORTH = 9.83
SOUTH = 5.92
EAST = 82.1
WEST = 79.6


def preprocessor(record):
    # check if price can be divided by landsize
    price = record.price
    land_size = record.land_size
    price_type = record.price_type
    land_type = record.land_type
    availability = record.land_availability
    location1 = record.location1
    location2 = record.location2
    house = 0
    beach = 0
    cultivate = 0
    tea = 0
    coconut= 0
    utilities = 0

    if record.price == 0:
        return

    if 'Perch' not in price_type and 'Acre' not in price_type:

        if land_size == 0:
            return
        #   elif record.size_type != ('perches' or 'acres' or 'square'):
        if record.size_type == 'perches':
            price = price/land_size
        else:
            return

        if record.size_type == 'acres':
            land_size = land_size*160
            price = price/land_size
        else:
            return

        if record.size_type == 'square':
            land_size = land_size/25.29
            price = price/land_size
        else:
            return

    if not land_type or land_type == 'Other':

        if wordappear(record, 'tea') == 1:
            land_type = 'Tea'
            tea = 1
        elif wordappear(record, 'coconut') == 1:
            land_type = 'Coconut'
            coconut = 1
        elif wordappear(record, 'paddy') == 1:
            land_type = 'Paddy'
            cultivate = 1
        elif wordappear(record, 'rubber') == 1:
            land_type = 'Rubber'
            cultivate = 1
        elif wordappear(record, 'cultivated') == 1:
            land_type = 'Cultivated'
            cultivate = 1
        elif wordappear(record, 'house') == 1:
            land_type = 'House'
            house = 1
        else:
            land_type = "Bare"

    else:
        if "Bare" in land_type:
            land_type = 'Bare'
        elif "Beachfront" in land_type:
            land_type = 'Beach'
            beach = 1
        elif "Cinnamon" in land_type:
            land_type = 'Cinnamon'
            cultivate = 1
        elif "Coconut" in land_type:
            land_type = 'Coconut'
            coconut = 1
        elif "Cultivated" in land_type:
            land_type = 'Cultivated'
            cultivate = 1
        elif "house" in land_type:
            land_type = 'House'
            house = 1
        elif "Paddy" in land_type:
            land_type = 'Paddy'
            cultivate = 1
        elif "Rubber" in land_type:
            land_type = 'Rubber'
            cultivate = 1
        elif "Tea" in land_type:
            land_type = 'Tea'
            tea = 1

    if wordappear(record, 'electricity') == 1:
        utilities = 1

    # binarize availabilty
    if "Reduced!" in availability:
         availability = 1
    elif "Urgent" in availability:
        availability = 1
    else:
        availability = 0


    clean_entry = ProcLandData(price = price, land_type = land_type, land_size=land_size,
                                   land_availability = availability , date_collected = record.date_collected,
                                   raw_id = record.id, house=house, beach=beach, cultivated=cultivate, tea=tea,
                                   coconut=coconut, utilities=utilities)

    try:
        GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

        if location2:
            address = location2 + " "+ location1
        else:
            address = location1

        address = address + ' Sri Lanka'

        params = {
            'address': address,
            'key': GOOGLE_MAPS_API_KEY,
        }
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()
        result = res['results'][0]

        latitude = result['geometry']['location']['lat']
        longitude = result['geometry']['location']['lng']


        if longitude > EAST or longitude < WEST:
            return
        elif latitude > NORTH or latitude< SOUTH:
            return

        clean_entry.latitude = latitude
        clean_entry.longitude = longitude

    except:
        try:
            address = location1+ 'Sri Lanka'
            params = {
                'address': address,
                'key': GOOGLE_MAPS_API_KEY,
            }
            req = requests.get(GOOGLE_MAPS_API_URL, params=params)
            res = req.json()
            result = res['results'][0]

            latitude = result['geometry']['location']['lat']
            longitude = result['geometry']['location']['lng']
            if longitude > EAST or longitude < WEST:
                return
            elif latitude > NORTH or latitude < SOUTH:
                return

            clean_entry.latitude = latitude
            clean_entry.longitude = longitude
        except:
            print('Couldnt get longitude and latitude')
            return


    clean_entry.save()

def wordappear(record, word):

    wholestring = record.about
    appear =0
    # wholestring = re.split('.|,|</p>|<br/>| ', wholestring)
    wholestring = wholestring.replace('.', '$')
    wholestring = wholestring.replace('</p>', '$')
    wholestring = wholestring.replace('<br/>', '$')
    # wholestring = wholestring.replace(',', '$')
    wholestring = wholestring.split('$')
    for wholer in wholestring:
        wholer = wholer.split(" ")
        for whole in wholer:
         if word.lower() in whole.lower() and len(word)==len(whole):
            appear =1

    return appear



def startprocess():


    try:
        records = RawLandData.objects.all()
        x = 0
        for record in records:
            x= x+1
            preprocessor(record)
    except:
        print ('finished pre processing data')



