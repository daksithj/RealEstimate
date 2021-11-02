from django.shortcuts import render, redirect
from django.urls import reverse
from .models import BacklogEntries, HouseBacklog, LandBacklog, ModelMeta, Importance, Location
from .GetValues import get_land_price, get_house_price
from .UpdateModel import update_model, reset_data
from .forms import UserRegisterForm
from django.contrib import messages
import locale
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'dataprocess/home.html')

def model(request):
    if request.POST:
       update_model()

    context = {'land': ModelMeta.objects.get(type='land'), 'house': ModelMeta.objects.get(type='house')}
    return render(request, 'dataprocess/model.html', context)

def analysis(request):

    context = {'location': Location.objects.all(), 'land_imp': Importance.objects.filter(type='land'),
               'house_imp': Importance.objects.filter(type='house')}
    return render(request, 'dataprocess/analysis.html', context)

@login_required
def update(request):
    if request.POST:
        if 'update_model' in request.POST:
            update_model()
        elif 'reset_data' in request.POST:
            reset_data()

    try:
        context = {'land': ModelMeta.objects.get(type='land')}
    except:
        context = None
    return render(request,'dataprocess/update.html', context)

@login_required
def register(request):
    if request.method == 'POST':
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}!')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request, 'dataprocess/register.html', {'form': form})


def get_land(request):
    if request.POST:
        address = request.POST['address']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        if request.POST['form-type'] == '1':
            land_size = float(request.POST['land-land_size'])
            cult = request.POST['cultivation']
            tea = 0
            coconut = 0
            cultivation = 0
            beach = 0
            utilities = 0
            land_availability = 0
            if cult =='tea':
                tea =1
            elif cult =='coconut':
                coconut = 1
            elif cult =='cultivation':
                cultivation = 1

            try :
                beach = int(request.POST['land-beach'])

            except:
                pass
            try :
                utilities = int(request.POST['land-utilities'])

            except:
                pass
            try :
                land_availability = int(request.POST['land-availability'])

            except:
                pass

            new_search = BacklogEntries(search_type=1)
            new_search.address = address
            new_search.save()
            seach_id = new_search.search_no

            new_land_search = LandBacklog(search_id=seach_id, latitude=latitude, longitude=longitude,
                                          land_size=land_size,land_availability=land_availability,
                                          coconut=coconut,tea=tea,cultivated=cultivation,
                                          beach=beach,utilities=utilities)


            search_detail = {'land_size': land_size, 'availability': land_availability,
                            'beach': beach, 'coconut': coconut, 'cultivated': cultivation, 'tea': tea,
                            'utilities': utilities, 'latitude':latitude, 'longitude':longitude}

            price = get_land_price(search_detail,0)
            temp_price = price/100000
            temp_price = round(temp_price)
            price = temp_price * 100000
            new_land_search.price = price
            new_land_search.save()



        else:
            land_size = float(request.POST['house-land_size'])
            floor_area = int(request.POST['house-floor_area'])
            bedrooms = int(request.POST['house-bedrooms'])
            bathrooms = int(request.POST['house-bathrooms'])
            parking = int(request.POST['house-parking'])
            floors = int(request.POST['house-floors'])
            water = int(request.POST['water'])
            electricity = int(request.POST['electricity'])
            overhead = int(request.POST['overhead'])
            furnished = int(request.POST['furnished'])

            p_garden = 0
            roof_garden = 0
            in_garden = 0
            hot_water = 0
            ac_rooms = 0
            garage = 0
            servant = 0
            pool = 0
            security = 0
            luxury = 0
            colonial = 0
            front = 0

            try :
                p_garden = int(request.POST['house-p_garden'])
            except:
                pass
            try :
                roof_garden = int(request.POST['house-roof_garden'])
            except:
                pass
            try :
                in_garden = int(request.POST['house-in_garden'])
            except:
                pass
            try :
                hot_water = int(request.POST['house-hot_water'])
            except:
                pass
            try :
                ac_rooms = int(request.POST['house-ac_rooms'])
            except:
                pass
            try :
                garage = int(request.POST['house-garage'])
            except:
                pass
            try :
                servant = int(request.POST['house-servant'])
            except:
                pass
            try :
                pool = int(request.POST['house-pool'])
            except:
                pass
            try :
                security = int(request.POST['house-security'])
            except:
                pass
            try :
                luxury = int(request.POST['house-luxury'])
            except:
                pass
            try :
                colonial = int(request.POST['house-colonial'])
            except:
                pass
            try :
                front = int(request.POST['house-front'])
            except:
                pass

            new_search = BacklogEntries(search_type=2)
            new_search.address = address
            new_search.save()
            seach_id = new_search.search_no


            new_house_search = HouseBacklog(search_id=seach_id, latitude=latitude, longitude=longitude,
                                          bedrooms=bedrooms,bathrooms=bathrooms, floor_area=floor_area,
                                          floors=floors, parking=parking, land_size=land_size,
                                          water=water, overhead=overhead, garage=garage, p_garden=p_garden,
                                          servant=servant, hot_water=hot_water,electricity=electricity,
                                          ac_rooms=ac_rooms,luxury=luxury, security=security,
                                          roof_garden=roof_garden,in_garden=in_garden,furnished=furnished,
                                          pool=pool,colonial=colonial,front=front)

            search_detail = {'bedrooms': bedrooms, 'bathrooms': bathrooms,  'floor_area': floor_area,
                            'parking': parking, 'p_garden': p_garden, 'land_size':land_size,
                            'servant': servant, 'ac_rooms': ac_rooms, 'luxury': luxury, 'colonial': colonial,
                            'water': water, 'electricity': electricity, 'floors': floors,
                            'hot_water': hot_water, 'overhead': overhead,
                            'garage': garage, 'roof_garden': roof_garden, 'pool': pool,
                            'in_garden': in_garden, 'security': security, 'furnished': furnished,
                            'front': front, 'latitude': latitude, 'longitude': longitude}

            price = get_house_price(search_detail)

            temp_price = price/100000
            temp_price = round(temp_price)
            price = temp_price * 100000
            new_house_search.price = price
            new_house_search.save()

        search_id = seach_id
        return redirect(reverse('price-report', args=(search_id,)))

    return render(request, 'dataprocess/landprice.html')


def show_report(request, search_id):
    locale.setlocale(locale.LC_ALL, 'en_US')
    search_form = BacklogEntries.objects.get(search_no=search_id)
    search_type = search_form.search_type
    address = search_form.address
    if search_type == 1:
        record = LandBacklog.objects.get(search_id=search_id)
        price = record.price * record.land_size
        price = locale.format_string("%d", price, grouping=True)

        features =[]

        if record.beach == 1:
            features.append("Beachfront property")
        if record.utilities == 1:
            features.append("Availability of electricity/water")
        if record.land_availability == 1:
            features.append("Discounted price/Urgent sale")

        land_type = "Bare Land"

        if record.tea ==1:
            land_type = "Tea cultivation"

        if record.coconut ==1:
            land_type = "Coconut cultivation"

        if record.cultivated ==1:
            land_type = "Other cultivations/ Multiple cultivations"


        context ={'type': 1, 'report':record, 'features': features, 'address' : address, 'price': price,
                  'land_type':land_type}

    else:
        record = HouseBacklog.objects.get(search_id=search_id)
        price = locale.format_string("%d", record.price, grouping=True)
        utilities = []

        if record.water ==1:
            utilities.append("Mainline water")
        if record.electricity ==1:
            utilities.append("3-Phase electricity")
        if record.overhead ==1:
            utilities.append("Overhead water tank")
        if record.furnished ==1:
            utilities.append("Fully furnished")

        garden =[]

        if record.p_garden==1:
            garden.append("Private Garden")
        if record.roof_garden==1:
            garden.append("Roof top Garden")
        if record.in_garden==1:
            garden.append("Indoor Garden")

        features =[]

        if record.hot_water == 1:
            features.append("Hot water")
        if record.ac_rooms == 1:
            features.append("A/C rooms")
        if record.garage == 1:
            features.append("Garage")
        if record.servant == 1:
            features.append("Servant rooms")
        if record.pool == 1:
            features.append("Swimming pool")
        if record.security == 1:
            features.append("24-hour Security/ Security system")

        house_type=[]

        if record.luxury == 1:
            house_type.append("Luxury design")
        if record.colonial == 1:
            house_type.append("Colonial architecture")
        if record.front == 1:
            house_type.append("Beachfront/ Riverfront/ Lakefront")

        context ={'type': 2, 'report':record, 'options': features,
                  'utilities': utilities, 'gardens': garden,
                  'housetypes': house_type, 'address': address, 'price': price}

    return render(request, 'dataprocess/report.html', context)
