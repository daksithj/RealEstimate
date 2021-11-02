from django.shortcuts import render, redirect
from .LankaPropHouses import startScrape

def land_scrape(request):
    if request.POST:
        # Run your script here
        startScrape()
    return render(request, 'webscrape/startscrape.html')

