from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from datetime import date, timedelta
from .models import RawLandData

baseURL = "https://www.lankapropertyweb.com/"

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

    details_containers = page_soup.findAll("div", {"class": "container grid"})[0]
    details_containers = details_containers.findAll("div", {"class": "row"})[1]
    details_containers = details_containers.findAll("div", {"class": "col-md-7 col-md-offset-1"})[0]
    #getting header information
    heading_containers = details_containers.findAll("div", {"class": "details-heading details-property"})[0]
    main_heading =  heading_containers.findAll("h1")[0].text.strip()
    #print(main_heading)
        #getting location
    loc_containers = heading_containers.findAll("div", {"class": "row"})[0]
    loc_containers = loc_containers.findAll("div", {"class": "col-md-9 col-sm-10 col-xs-12"})[0]
    location = loc_containers.findAll("span", {"class": "details-location"})[0].text.strip()
    #print( location)
        #getting price
    price_containers = heading_containers.findAll("div", {"class": "row"})[1]
    price_containers = price_containers.findAll("div", {"class": "price-detail"})[0]
    price = price_containers.contents[0]
    #print (price)
    price_type = price_containers.findAll("span", {"class": "price-type"})[0].text.strip()
    #print (price_type)

    # getting body information
    body_containers = details_containers.findAll("div", {"class": "row details-property"})[0]

        #info containers
    info_containers = body_containers.findAll("div", {"class": "col-lg-12 important green-borders"})[0]
    info_containers = info_containers.findAll("div", {"class": "row"})[0]
    prop_containers = info_containers.findAll("div", {"class": "col-md-6 col-sm-6"})[0]
    prop_containers = prop_containers.findAll("table")[0]
    #prop_containers = prop_containers.findAll("tbody")[0]
    table_containers = prop_containers.findAll("tr")[0]
    land_type = table_containers.findAll("td", {"class": "right"})[0].text.strip()
    #print(land_type)
    table_containers = prop_containers.findAll("tr")[1]
    land_size = table_containers.findAll("td", {"class": "right"})[0].text.strip()
    #print(land_size)
    prop_containers = info_containers.findAll("div", {"class": "col-md-6 col-sm-6"})[1]
    prop_containers = prop_containers.findAll("table")[0]
    #prop_containers = prop_containers.findAll("tbody")[0]
    table_containers = prop_containers.findAll("tr")[0]
    land_availability = table_containers.findAll("td", {"class": "right"})[0].text.strip()
    #print(land_availability)



    #getting details
    about_containers = body_containers.findAll("div", {"class": "col-lg-12 about-section"})[0]
    about_containers = about_containers.findAll("div", {"class": "row"})[0]
    about_containers = about_containers.findAll("div", {"class": "col-lg-12"})[0]
    about_containers = about_containers.findAll("div", {"class": "details-heading"})[0]
    land_about = about_containers.findAll("p")[0]
    #print(land_about)

    #getting date posted
    #print(body_containers.name)
    #print(soup.prettify(body_containers))
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

    if price ==0:
        #print("price is 0")
        return


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

    if not location1 and not location2:
        #print("location not available")
        return

    #land size
    try:
        land_size = land_size.split()
        size = land_size[0]
        try:
            size = float(size)
        except:
            size = 0
        try:
            size_type = land_size[1]
        except:
            size_type = None
    except:
        size = None
        size_type = None



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

    # print(main_heading)
    # print(price)
    # print(price_type)#
    # print(size)
    # print(size_type)
    # print(location1)
    # print(location2)#
    # print(date_posted)
    # print(land_type)
    # print(land_availability)
    # print(land_about)

    newentry = RawLandData(price= price)
    newentry.heading = main_heading
    newentry.price_type = price_type
    if size:
        newentry.land_size = size
    if size_type:
        newentry.size_type = size_type
    if location1:
     newentry.location1 = location1

    if location2:
        newentry.location2 = location2
    if date_posted:
        newentry.date_collected = date_posted

    newentry.land_type = land_type
    newentry.land_availability = land_availability
    newentry.about = land_about

    newentry.save()

def startScrape():
    #url to store barelands search page
    bareland_url= baseURL + "/land/index.php"

    get_Adds(bareland_url, 0)

def updateScrape():
    pass
