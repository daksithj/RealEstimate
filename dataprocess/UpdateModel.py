import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from .models import ProcLandData, ProcHouseData, ModelMeta, Importance, Location
from webscrape.LankaProperty import startScrape as start_land
from webscrape.LankaProperty import scrapeAdd as update_land
from webscrape.LankaPropHouses import startScrape as start_house
from webscrape.LankaPropHouses import scrapeAdd as update_house
from .LandPreProc import startprocess as pre_land
from .HousePreProc import startprocess as pre_house
from .LandPreProc import preprocessor as land_pre
from .HousePreProc import preprocessor as house_pre
from webscrape.models import RawLandData, RawHouseData
import pickle
import feedparser
from datetime import datetime
from time import mktime
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def clusterize():


    land = pd.DataFrame(list(ProcLandData.objects.all().values()))
    house = pd.DataFrame(list(ProcHouseData.objects.all().values()))

    land['price'] = np.log(land['price'])
    house['price'] = np.log(house['price'])
    land = land[np.abs(land.price - land.price.mean()) <= (3 * land.price.std())]
    land = land.reset_index(drop=True)
    house = house[np.abs(house.price - house.price.mean()) <= (3 * house.price.std())]
    house = house.reset_index(drop=True)
    land = land.drop(['id'], 1)
    house = house.drop(['id'], 1)

    la = np.array(land[['latitude','longitude']].astype(float))
    ho = np.array(house[['latitude','longitude']].astype(float))

    z = np.append(la, ho, axis=0)

    kmeans = KMeans(n_clusters=1500)
    kmeans.fit(z)

    with open('model/km_both.sav', 'wb') as f:
        pickle.dump(kmeans, f)

    ModelMeta.objects.all().delete()
    Importance.objects.all().delete()
    Location.objects.all().delete()

def generate_land_model():
    with open('model/km_both.sav', 'rb') as f:
        kmeans = pickle.load(f)

    data = pd.DataFrame(list(ProcLandData.objects.all().values()))

    data = data.drop(['id', 'raw_id', 'date_collected', 'land_type',
                     ], 1)
    data['price'] = np.log(data['price'])
    data = data[np.abs(data.price - data.price.mean()) <= (3 * data.price.std())]
    data = data.reset_index(drop=True)

    km = np.array(data[['latitude','longitude']].astype(float))
    clust_labels = kmeans.predict(km)
    centroids = kmeans.cluster_centers_
    tmeans = pd.DataFrame(clust_labels)
    data.insert((data.shape[1]), 'kmeans', tmeans)

    header_list=['lat', 'long', 'price']
    center = pd.DataFrame(list(centroids))
    center['price']=""
    brain = []

    for x in clust_labels:
        av = data.loc[data['kmeans'] == x]['price'].mean()
        brain.append(av)

        center.at[x, 'price']= np.exp(av)



    cen =[]
    for index, row in center.iterrows():

        cent = Location(latitude=row[0], longitude=row[1])

        if isinstance(row['price'], str):
            cent.price = 0
        else:
            cent.price=row['price']
        cen.append(cent)

    Location.objects.bulk_create(cen)

    li = {"avg": brain}
    df = pd.DataFrame(data=li)
    data.insert((data.shape[1]), 'avg', df)

    save_df = data.filter(['kmeans', 'avg'], axis=1)
    save_df.to_pickle('model/land_avg.sav')

    labels = np.array(data['price'])
    features = data.drop(['price', 'kmeans', 'latitude', 'longitude'], axis=1)

    feature_list = list(features.columns)
    # print(feature_list)
    features = np.array(features)

    # split dataset to 75 training 25 test
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25,
                                                                                random_state=42)
    rf = RandomForestRegressor(n_estimators=500, random_state=42)
    rf.fit(train_features, train_labels)

    # Make predictions and determine the error
    predictions = rf.predict(test_features)
    importances = rf.feature_importances_

    for i , s in enumerate(feature_list):

        feature_list[i] = feature_list[i].replace('_', ' ')
        feature_list[i] = feature_list[i].title()


    sorted_feature_importance = sorted(zip(importances, list(feature_list)), reverse=True)
    sorted_feature_importance.pop(0)
    sorted_feature_importance.pop(0)


    for imp in sorted_feature_importance:
        imp_list = Importance(type='land')
        imp_list.importance = imp[0]
        imp_list.feature = imp[1]
        imp_list.save()


    entry = ModelMeta(type='land')


    errors = abs(predictions - test_labels)
    # Display the performance metrics
    # print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')
    mae = round(np.mean(errors), 2)
    mape = np.mean(100 * (errors / test_labels))
    accuracy = 100 - mape
    accuracy = round(accuracy, 2)
    # print('Accuracy:', round(accuracy, 2), '%.')

    entry.training_num = train_labels.size
    entry.test_num = test_labels.size
    entry.accuracy = accuracy
    entry.MAE = mae
    entry.save()

    with open('model/rf_land.sav', 'wb') as f:
        pickle.dump(rf, f)


def generate_house_model():
    data = pd.DataFrame(list(ProcHouseData.objects.all().values()))
    with open('model/km_both.sav', 'rb') as f:
        kmeans = pickle.load(f)

    data = data.drop(['id', 'raw_id', 'brand_new', 'km'], 1)

    km = np.array(data[['latitude','longitude']].astype(float))
    clust_labels = kmeans.predict(km)
    clus = pd.DataFrame(clust_labels)
    data.insert((data.shape[1]), 'kmeans', clus)

    for row in data.itertuples():
        if not row.avg:
            data.drop(row.Index, inplace=True)

    brain = []
    for row in data.itertuples():
        x = row.kmeans
        mean = (data.loc[data['kmeans'] == x]['avg'].median())
        brain.append(mean)

    li = {"avg": brain}
    df = pd.DataFrame(data=li)
    data.insert((data.shape[1]), 'near', df)
    data = data.reset_index(drop=True)

    data = data.reset_index(drop=True)
    data['avg'] = data['near']*data['land_size']
    data['price'] = data['price'] - data['avg']
    data = data[data.price > 0]
    data['price'] = np.log(data['price'])
    data = data[np.abs(data.price - data.price.mean()) <= (3 * data.price.std())]
    data = data.reset_index(drop=True)

    labels = np.array(data['price'])
    features = data.drop(['price', 'kmeans', 'latitude', 'longitude',  'land_availability', 'avg', 'land_size', 'near'],
                         axis=1)
    feature_list = list(features.columns)
    # print(feature_list)
    features = np.array(features)

    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25,
                                                                                random_state=42)

    rf = RandomForestRegressor(n_estimators=300, random_state=42)

    rf.fit(train_features, train_labels)

    # Make predictions and determine the error
    predictions = rf.predict(test_features)

    importances = rf.feature_importances_

    for i , s in enumerate(feature_list):

        feature_list[i] = feature_list[i].replace('_', ' ')
        feature_list[i] = feature_list[i].title()

    sorted_feature_importance = sorted(zip(importances, list(feature_list)), reverse=True)
    sorted_feature_importance.pop(0)
    for imp in sorted_feature_importance:
        imp_list = Importance(type='house')
        imp_list.importance = imp[0]
        imp_list.feature = imp[1]
        imp_list.save()

    entry = ModelMeta(type='house')


    errors = abs(predictions - test_labels)
    # Display the performance metrics
    # print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')
    mae = round(np.mean(errors), 2)
    mape = np.mean(100 * (errors / test_labels))
    accuracy = 100 - mape
    accuracy = round(accuracy, 2)
    # print('Accuracy:', round(accuracy, 2), '%.')

    entry.training_num = train_labels.size
    entry.test_num = test_labels.size
    entry.accuracy = accuracy
    entry.MAE = mae
    entry.save()

    with open('model/rf_house.sav', 'wb') as f:
        pickle.dump(rf, f)


def update_data():
    d = feedparser.parse('https://www.lankapropertyweb.com/feeds/latest_rss.xml')

    dater = RawLandData.objects.last()
    dater= dater.date_collected
    dt = datetime.fromtimestamp(mktime(d.entries[0].published_parsed))

    if dt.date() <= dater.date():

        return


    for feed in d.entries:
        link = feed.link
        broken = link.split('/')
        if "land" in broken:

            try:
                update_land(link)
                last = RawLandData.objects.last()
                land_pre(last)
            except:
                pass
        if "sale" in broken:
            try:
                update_house(link)
                last = RawHouseData.objects.last()
                house_pre(last)
            except:
                pass

def update_model():


    update_data()

    clusterize()
    generate_land_model()
    generate_house_model()

def reset_data():

    RawHouseData.objects.all().delete()
    RawLandData.objects.all().delete()
    ProcLandData.objects.all().delete()
    ProcHouseData.objects.all().delete()

    start_land()
    start_house()
    pre_land()
    pre_house()

    update_model()
