from webscrape.models import RawHouseData
import pandas as pd
import numpy as np
from .models import ProcLandData, ProcHouseData
from .GetValues import get_land_price

import requests



# api key : AIzaSyC4pgdGcQIgG4_Pf6I4hlYq2GrygqaAFgo
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
GOOGLE_MAPS_API_KEY =  'AIzaSyC4pgdGcQIgG4_Pf6I4hlYq2GrygqaAFgo'
NORTH = 9.83
SOUTH = 5.96
EAST = 82.1
WEST = 79.6
count =0


def preprocessor(record):

    global count

    id = record.id
    price = record.price
    land_size = record.land_size
    bedrooms = record.bedrooms
    bathrooms = record.bathrooms
    floor_area = record.floor_area
    floors = record.floors
    parking = record.parking
    land_size = record.land_size
    availability = record.land_availability
    location1 = record.location1
    location2 = record.location2
    features = record.features
    about = record.about


    if price == 0:
        return

    data = pd.DataFrame(list(RawHouseData.objects.all().values()))
    data = data.loc[data['id'] != id]
    data = data.loc[data['price'] > 0]
    data['price'] = np.log(data['price'])
    mean = data['price'].mean()
    std = data['price'].std()
    min_price = np.exp(mean - 3 * std)
    max_price = np.exp(mean + 3 * std)
    mean_price = np.exp(mean)

    if price < min_price or price > max_price:
        return


    #bedroome

    if bedrooms >= 5:

        wholestring = record.about.lower()
        appear = 0
        # wholestring = re.split('.|,|</p>|<br/>| ', wholestring)
        wholestring = wholestring.replace('.', '$')
        wholestring = wholestring.replace('</p>', '$')
        wholestring = wholestring.replace('<br/>', '$')
        # wholestring = wholestring.replace(',', '$')
        wholestring = wholestring.split('$')
        try:
            for wholer in wholestring:
                wholer = wholer.split(" ")
                i = 0
                while i < len(wholer):
                    if 'bed' in wholer[i]:
                        if wholer[i-1].isdigit():
                            if int(wholer[i-1])>bedrooms and int(wholer[i-1])<10:
                                bedrooms = int(wholer[i-1])
                        break
                    i = i + 1
        except:
            pass


    #floor area
    data = pd.DataFrame(list(RawHouseData.objects.all().values()))
    data = data.loc[data['id'] != id]
    data = data.loc[data['bedrooms'] == bedrooms]
    data = data.loc[data['bathrooms'] == bathrooms]
    data = data.loc[data['floor_area'] > 0]
    data['floor_area']= np.log(data['floor_area'])
    mean = data['floor_area'].mean()
    std = data['floor_area'].std()

    min_area = np.exp(mean - 1 * std)
    tolmin_area = np.exp(mean - 0.75 * std)
    max_area = np.exp(mean + 1 * std)
    tolmax_area = np.exp(mean + 0.75 * std)
    mean = np.exp(mean)

    # print(id)
    # print(floor_area)
    # print (min_area)
    # print(mean)
    # print(max_area)
    # print('--------')

    if floor_area == 0 or not floor_area:
        if land_size!=0:
            land_mean = land_size*272.25*floors
            if mean < land_mean:
                floor_area =mean
            elif mean > land_mean:
                floor_area = land_mean
            else:
                return
        else:
            floor_area = mean

    if floor_area <500 and floor_area <= land_size*floors:
        floor_area = floor_area *272.25


    try:
        if floor_area > tolmax_area:
            if floor_area < max_area:
                floor_area = tolmax_area
            else:

                return
        if floor_area < tolmin_area:
            if floor_area > min_area:
                    floor_area = tolmin_area
            else:

                    return

    except:

        return


    if floors > 4:
        return

    if parking >=20:
        return

    if land_size > 2*floor_area/(272.25*floors):
        if  land_size/272.25 >= floor_area/(272.25*floors):
            land_size = land_size/272.25
        else:
            land_size = floor_area/(272.25*floors)
    elif land_size < floor_area/(272.25*floors):
        land_size = floor_area / (272.25 * floors)


    if land_size<1 or land_size > 50:
        return

    if not floor_area:
        return

    #binarize availabilty
    if "Reduced!" in availability:
         availability = 1
    elif "Urgent" in availability:
        availability = 1
    else:
        availability = 0

    entry = ProcHouseData(price = price)
    entry.bedrooms = bedrooms
    entry.bathrooms = bathrooms
    entry.floor_area = floor_area
    entry.floors = floors
    entry.parking = parking
    entry.land_size=land_size
    entry.land_availability = availability
    entry.raw_id = id

    if "mainline water" in features:
        entry.water =1
    if "overhead water storage" in features:
        entry.overhead =1
    if "garage" in features:
        entry.garage =1
    if "private garden" in features:
        entry.p_garden = 1
    if "servant" in features:
        entry.servant = 1
    if "hot water" in features:
        entry.hot_water = 1
    if "3 phase electricity" in features:
        entry.electricity= 1
    if "ac rooms" in features:
        entry.ac_rooms = 1
    if "luxury" in features:
        entry.luxury = 1
    if "brand new " in features:
        entry.brand_new = 1
    if "security" in features:
        entry.security = 1
    if "roof top garden" in features:
        entry.roof_garden = 1
    if "indoor garden" in features:
        entry.in_garden = 1
    if "furnished" in features:
        entry.furnished = 1
    if "swimming pool" in features:
        entry.pool = 1
    if "colonial" in features:
        entry.colonial = 1
    if "waterfront" in features:
        entry.front = 1
    if "riverside" in features:
        entry.front = 1
    if "beachfront" in features:
        entry.front = 1
    if "sea view" in features:
        entry.front = 1

    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    try:


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

        entry.latitude = latitude
        entry.longitude = longitude
    except:
        pass

    if not entry.latitude or not entry.longitude:
        try:
            address = location1 + 'Sri Lanka'
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

            entry.latitude = latitude
            entry.longitude = longitude

        except:
            print('Couldnt get longitude and latitude')
            return




    d = {'land_size': land_size, 'availability': availability,
         'front': entry.front, 'latitude': entry.latitude, 'longitude': entry.longitude}
    try:
        price = get_land_price(d, 1)
        avg = price
        record.save()
    except:
        return

    if avg > price or avg == 0:
        return
    else:
        entry.avg = avg

    entry.save()


def startprocess():

    try:
        records = RawHouseData.objects.all()
        #print(records)
        for record in records:

            preprocessor(record)
            # print(record.id)
    except:
        print("Completed pre processing house")
