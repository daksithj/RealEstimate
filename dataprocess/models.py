from django.db import models
from webscrape.models import RawLandData, RawHouseData
from django.utils import timezone
from django.contrib.auth.models import User


class ProcLandData(models.Model):
    price = models.IntegerField(default = 0, null = True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    land_type = models.CharField(max_length=20, null = True)
    land_size = models.FloatField(default = 0, null = True)
    land_availability = models.BooleanField(default=0)
    date_collected= models.DateTimeField(default= timezone.now, null = True)
    raw = models.ForeignKey(RawLandData, null=True, on_delete=models.SET_NULL)
    coconut = models.IntegerField(default =0)
    tea = models.IntegerField(default=0)
    cultivated = models.IntegerField(default=0)
    house = models.IntegerField(default=0)
    beach = models.IntegerField(default=0)
    utilities = models.IntegerField(default=0)


    def __str__(self):
        return self.id

class ProcHouseData(models.Model):
    price = models.FloatField(default = 0, null = True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    bedrooms = models.IntegerField(default=1, null=True)
    bathrooms= models.IntegerField(default=1, null=True)
    floor_area = models.FloatField(default=0, null=True)
    floors = models.IntegerField(default=1, null=True)
    parking = models.IntegerField(default=0, null=True)
    land_size = models.FloatField(default = 0, null = True)
    land_availability = models.CharField(max_length=20, null = True)
    water = models.IntegerField(default=0, null=True)
    overhead = models.IntegerField(default=0, null=True)
    garage = models.IntegerField(default=0, null=True)
    p_garden = models.IntegerField(default=0, null=True)
    servant = models.IntegerField(default=0, null=True)
    hot_water = models.IntegerField(default=0, null=True)
    electricity = models.IntegerField(default=0, null=True)
    ac_rooms = models.IntegerField(default=0, null=True)
    luxury = models.IntegerField(default=0, null=True)
    brand_new = models.IntegerField(default=0, null=True)
    security = models.IntegerField(default=0, null=True)
    roof_garden = models.IntegerField(default=0, null=True)
    in_garden = models.IntegerField(default=0, null=True)
    furnished = models.IntegerField(default=0, null=True)
    pool = models.IntegerField(default=0, null=True)
    colonial = models.IntegerField(default=0, null=True)
    front = models.IntegerField(default=0, null=True)
    raw = models.ForeignKey(RawHouseData, null=True, on_delete=models.SET_NULL)
    avg = models.FloatField(default=0, null=True)
    km = models.IntegerField(null=True)


class BacklogEntries(models.Model):
    search_no = models.AutoField(primary_key=True)
    search_type = models.IntegerField(default=0)
    address = models.TextField(null =True)
    date_searched = models.DateTimeField(auto_now_add=True, blank=True)


class HouseBacklog(models.Model):
    search = models.ForeignKey(BacklogEntries, on_delete=models.CASCADE)
    price = models.FloatField(default=0, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    bedrooms = models.IntegerField(default=1, null=True)
    bathrooms= models.IntegerField(default=1, null=True)
    floor_area = models.FloatField(default=0, null=True)
    floors = models.IntegerField(default=1, null=True)
    parking = models.IntegerField(default=0, null=True)
    land_size = models.FloatField(default = 0, null = True)
    water = models.IntegerField(default=0, null=True)
    overhead = models.IntegerField(default=0, null=True)
    garage = models.IntegerField(default=0, null=True)
    p_garden = models.IntegerField(default=0, null=True)
    servant = models.IntegerField(default=0, null=True)
    hot_water = models.IntegerField(default=0, null=True)
    electricity = models.IntegerField(default=0, null=True)
    ac_rooms = models.IntegerField(default=0, null=True)
    luxury = models.IntegerField(default=0, null=True)
    security = models.IntegerField(default=0, null=True)
    roof_garden = models.IntegerField(default=0, null=True)
    in_garden = models.IntegerField(default=0, null=True)
    furnished = models.IntegerField(default=0, null=True)
    pool = models.IntegerField(default=0, null=True)
    colonial = models.IntegerField(default=0, null=True)
    front = models.IntegerField(default=0, null=True)


class LandBacklog(models.Model):

    search = models.ForeignKey(BacklogEntries, on_delete=models.CASCADE)
    price = models.FloatField(default=0, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    land_size = models.FloatField(default = 0, null = True)
    land_availability = models.BooleanField(default=0)
    coconut = models.IntegerField(default =0)
    tea = models.IntegerField(default=0)
    cultivated = models.IntegerField(default=0)
    beach = models.IntegerField(default=0)
    utilities = models.IntegerField(default=0)


class ModelMeta(models.Model):

    type = models.CharField(primary_key=True, max_length=10)
    last_date = models.DateTimeField(auto_now_add=True, blank=True)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    MAE = models.DecimalField(max_digits=5, decimal_places=2)
    training_num = models.IntegerField(default=0)
    test_num = models.IntegerField(default=0)

class Importance(models.Model):

    type = models.CharField(max_length=10)
    feature = models.CharField(max_length=20)
    importance = models.DecimalField(max_digits=5, decimal_places=4)

class Location(models.Model):

    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    price = models.FloatField(default=0, null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

