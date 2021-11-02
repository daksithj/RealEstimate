import pickle
import pandas as pd
import numpy as np


def get_land_price(details, lorh):
    with open('dataprocess/model/km_both.sav', 'rb') as f:
        kmeans = pickle.load(f)

    with open('dataprocess/model/rf_land.sav', 'rb') as f:
        rf = pickle.load(f)

    data = pd.read_pickle('dataprocess/model/land_avg.sav')

    d = {'latitude': [details['latitude']],
         'longitude': [details['longitude']]}
    df = pd.DataFrame(data=d)
    k_m = np.array(df.astype(float))
    km = kmeans.predict(k_m)

    if lorh:
        d = {'land_size': [details['land_size']], 'land_availability': [0],
             'beach': [details['front']], 'coconut': [0], 'cultivated': [0], 'house': [1], 'tea': [0], 'utilities': [1],
             'avg': [data.loc[data['kmeans'] == km[0]]['avg'].mean()]}
    else:
        d = {'land_size': [details['land_size']], 'land_availability': [details['availability']],
             'beach': [details['beach']],
             'coconut': [details['coconut']], 'cultivated': [details['cultivated']], 'house': [0],
             'tea': [details['tea']], 'utilities': [details['utilities']],
             'avg': [data.loc[data['kmeans'] == km[0]]['avg'].mean()]}

    df = pd.DataFrame(data=d)
    pred = np.array(df)

    prediction = rf.predict(pred)
    prediction = np.exp(prediction)

    return prediction[0]


def get_house_price(details):

    with open('dataprocess/model/rf_house.sav', 'rb') as f:
        rf = pickle.load(f)

    t = {'land_size': details['land_size'], 'availability': 0, 'beach': 0,
         'coconut': 0, 'cultivated': 0, 'house': 1, 'tea': 0, 'utilities': 0,
         'latitude': details['latitude'], 'longitude': details['longitude']}
    avg = (get_land_price(t, 0))

    d = {'bedrooms': [details['bedrooms']], 'bathrooms': [details['bathrooms']],  'floor_area': [details['floor_area']],
         'parking': [details['parking']], 'p_garden': [details['p_garden']],
         'servant': [details['servant']], 'ac_rooms': [details['ac_rooms']], 'luxury': [details['luxury']],
         'colonial': [details['colonial']],
         'water': [details['water']], 'electricity': [details['electricity']], 'floors': [details['floors']],
         'hot_water': [details['hot_water']], 'overhead': [details['overhead']],
         'garage': [details['garage']], 'roof_garden': [details['roof_garden']], 'pool': [details['pool']],
         'in_garden': [details['in_garden']], 'security': [details['security']], 'furnished': [details['furnished']],
         'front': [details['front']]}

    df = pd.DataFrame(data=d)
    pred = np.array(df)
    avg = (avg * details['land_size'])
    prediction = rf.predict(pred)
    prediction = np.exp(prediction) + avg

    return prediction[0]
