from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from datetime import date, timedelta
import collections
from .models import RawHouseData

baseURL = "https://www.lankapropertyweb.com/"

words =[]
def get_Adds(target_url, iteration):
    #reading search page
    uClient = uReq(target_url)
    land_search_html = uClient.read()
    uClient.close()

    #parsing the page
    page_soup = soup(land_search_html, "html.parser",from_encoding="iso-8859-1")

    #finding all property entries
    search_containers = page_soup.findAll("div", {"class": "adds-wrapper"})
    search_containers=search_containers[0]
    search_containers=search_containers.findAll("div", {"class": "tab-content"})
    search_containers=search_containers[0]
    search_containers=search_containers.findAll("div", {"class": "tab-pane fade active in"})
    search_containers=search_containers[0]
    search_containers=search_containers.findAll("div", {"class": "row"})
    search_containers=search_containers[0]
    search_containers=search_containers.findAll("section", {"class": "row items"})
    search_containers=search_containers[0]
    search_containers=search_containers.findAll("article", {"class": "item col-xs-1 gap"})
    #print(len(search_containers))

    #print(soup.prettify(search_containers[0].div.div.div.section.article))
    #print(searchpage.div["tab-content"])
    EnterAdd(search_containers)

    print ('Iteration' +str(iteration) + 'complete')
    next_containers = page_soup.findAll("ul", {"class": "pagination"})[0]

    try:
        next_containers = next_containers.findAll("li", {"class": "pagination_arrows"})[1]
        next_containers = next_containers.findAll("a")[0]['href']
        get_Adds(baseURL + next_containers, iteration+1)
    except:
        print('Scraping Complete')
        return

def EnterAdd(search_containers):

    for search in search_containers:
        link = baseURL + search.findAll("a")[0]['href']
        #print(link)
        scrapeAdd(link)

def scrapeAdd(target_url):
    # reading search page
    uClient = uReq(target_url)
    land_add_html = uClient.read()
    uClient.close()

    # parsing the page
    page_soup = soup(land_add_html, "html.parser", from_encoding="iso-8859-1")
    #print(soup.prettify( page_soup))
    details_containers = page_soup.findAll("div", {"class": "container grid"})[0]
    details_containers = details_containers.findAll("div", {"class": "row"})[1]
    details_containers = details_containers.findAll("div", {"class": "col-md-7 col-md-offset-1"})[0]
    #getting header information
    heading_containers = details_containers.findAll("div", {"class": "details-heading details-property"})[0]
    main_heading =  heading_containers.findAll("h1")[0].text.strip()
    #print(main_heading)
        #getting location
    #print(soup.prettify(heading_containers))
    #loc_containers = heading_containers.findAll("div", {"class": "row"})[1]

    loc_containers = page_soup.findAll("div", {"class": "col-md-9 col-sm-10 col-xs-12"})[0]
    location = loc_containers.findAll("span", {"class": "details-location"})[0].text.strip()
    #print( location)
        #getting price
    #price_containers = heading_containers.findAll("div", {"class": "row"})[1]
    price_containers = page_soup.findAll("div", {"class": "price-detail"})[0]
    price = price_containers.contents[0]
    #print (price)


    # getting body information
    body_containers = page_soup.findAll("div", {"class": "row details-property"})[0]

        #info containers
    info_containers = body_containers.findAll("div", {"class": "col-lg-12 important green-borders"})[0]
    info_containers = info_containers.findAll("div", {"class": "row"})[0]
    prop_containers = info_containers.findAll("div", {"class": "col-md-6 col-sm-6"})[0]
    prop_containers = prop_containers.findAll("table")[0]
    table_containers = prop_containers.findAll("tr")[0]
    property_type = table_containers.findAll("td", {"class": "right"})[0].text.strip()
    #print(property_type)
    table_containers = prop_containers.findAll("tr")[1]
    bedrooms = table_containers.findAll("td", {"class": "right"})[0].text.strip()
    #print(bedrooms)
    table_containers = prop_containers.findAll("tr")[2]
    bathrooms = table_containers.findAll("td", {"class": "right"})[0].text.strip()
    #print(bathrooms)
    table_containers = prop_containers.findAll("tr")[3]
    floor_area = table_containers.findAll("td", {"class": "right"})[0].text.strip()
    #print(floor_area)
    table_containers = prop_containers.findAll("tr")[4]
    floors = table_containers.findAll("td", {"class": "right"})[0].text.strip()
    #print(floors)
    table_containers = prop_containers.findAll("tr")[5]
    parking = table_containers.findAll("td", {"class": "right"})[0].text.strip()
    #print(parking)
    table_containers = prop_containers.findAll("tr")[6]
    land_size = table_containers.findAll("td", {"class": "right"})[0].text.strip()
    #print(land_size)
    prop_containers = info_containers.findAll("div", {"class": "col-md-6 col-sm-6"})[1]
    prop_containers = prop_containers.findAll("table")[0]
    table_containers = prop_containers.findAll("tr")[0]
    land_availability = table_containers.findAll("td", {"class": "right"})[0].text.strip()
    #print(land_availability)



    #getting details
    about_containers = body_containers.findAll("div", {"class": "col-lg-12 about-section"})[0]
    about_containers = about_containers.findAll("div", {"class": "row"})[0]
    about_containers = about_containers.findAll("div", {"class": "col-lg-12"})[0]
    det_about_containers = about_containers.findAll("div", {"class": "details-heading"})[0]
    land_about = det_about_containers.findAll("p")[0]
    #print(land_about)


    fea_about_cointainers = about_containers.findAll("div", {"class": "details-features"})[0]
    fea_about_cointainers = fea_about_cointainers.findAll("div", {"class": "row"})[0]
    fea_about_cointainers = fea_about_cointainers.findAll("div", {"class": "col-lg-4 col-md-4 col-sm-4"})
    features=[]
    for cont in fea_about_cointainers:
        cont = cont.findAll("table")[0]
        cont = cont.findAll("tr")
        #print(len(cont))
        for t in cont:
            toll = t.findAll("td", {"class": "first"})[0].text.strip()
            toll = toll.lower()
            features.append(toll)
            words.append(toll)


    #print(land_about)

    #getting date posted
    # print(body_containers.name)
    # print(soup.prettify(body_containers))col-lg-4 col-md-4 col-sm-4

    try:
        date_containers = body_containers.findAll(lambda tag: tag.name == 'div' and tag.get('class') == ['col-lg-12'], recursive=False)[0]
        date_containers = date_containers.findAll("div", {"class": "col-lg-12 form-wrap"})[0]
        date_containers = date_containers.findAll("div", {"class": "row"})[1]
        #print(soup.prettify(date_containers))
        date_containers = date_containers.findAll("div", {"class": "col-lg-12"})[0]
        date_posted = date_containers.findAll("div", {"class": "col-md-6 col-sm-6"})[0].text.strip()

    except:
        date_posted = None




   #cleaning data
    #price
    price = price.replace('Rs. ', '')
    price = price.replace(',', '')
    try:
        price = float(price)
    except:
        price = 0

    #location
    try:
        location = location.split(',')
        for loc in location:
            loc = loc.replace(' ', '')

        location1 = location.pop().lstrip()

        if location:
            location2 = location.pop().lstrip()
        else:
            location2= None
    except:
        location1=None
        location2=None

    #land size
    try:
        num =""
        dig = 0
        dec =0
        for s in land_size:

            if s.isdigit():
                dig = 1
                num = num+s
            else:
                if dig==1 and s!='.':
                    break
                elif s=='.' and dec==0 and dig==1:
                    num = num + s
                    dec =1
                elif s=='.' and dec ==1:
                    break
        try:
            size = float(num)
        except:
            size = 0

    except:
        size = None





    #dateposted

    if date_posted:
        date_posted = date_posted.split()
        if date_posted[1] == "Today":
            date_posted =0
        elif date_posted[1]  == "Yesterday":
            date_posted = 1
        else:
            date_posted = int(date_posted[1])

        date_posted = date.today() - timedelta(date_posted)

    else:
        date_posted = None

    land_about = ''.join((c for c in str(land_about) if ord(c) < 128))


    #bedrooms
    rooms = 0
    for x in bedrooms:
        if x.isdigit():
            rooms = x
            break
    bedrooms = rooms

    #bathrooms
    rooms = 0
    for x in bathrooms:
        if x.isdigit():
            rooms = x
            break
    bathrooms = rooms

    #floor area
    try:
        num = ""
        dig = 0

        for s in floor_area:
            if s.isdigit():
                dig = 1
                num = num + s
            else:
                if dig == 1:
                    break

        try:
            floor_area = float(num)
        except:
            floor_area = 0

    except:
        floor_area = None



    #features
    features = "$".join(features)

    # print(main_heading)
    # print(price)
    # print(property_type)
    # print(size)
    # print(floor_area)
    # print(floors)
    # print(bedrooms)
    # print(bathrooms)
    # print(parking)
    # print(location1)
    # print(location2)
    # print(date_posted)
    # print(land_availability)
    # print(features)
    #print(land_about)

    newentry = RawHouseData(price= price)
    newentry.heading = main_heading

    if size:
        newentry.land_size = size

    if location1:
        newentry.location1 = location1
    else:
        return
    if location2:
        newentry.location2 = location2
    if date_posted:
        newentry.date_collected = date_posted

    if property_type:
        property_type = property_type.lower()
        newentry.property_type = property_type
    else:
        newentry.property_type = "house"
    newentry.land_availability = land_availability
    newentry.about = land_about
    if bathrooms:
        newentry.bathrooms = bathrooms
    if bedrooms:
        newentry.bedrooms = bedrooms
    if floors:
        newentry.floors = floors
    newentry.floor_area = floor_area
    if parking:
        newentry.parking = parking
    newentry.features = features
    newentry.save()


def startScrape():

    # url to store houses search page
    bareland_url= baseURL + "/sale/forsale-all-House.html"

    get_Adds(bareland_url, 0)
    counter = collections.Counter(words)
    #text_file = open("KeyOutput.txt", "w")
    #text_file.write(counter.most_common())
    #text_file.close()
