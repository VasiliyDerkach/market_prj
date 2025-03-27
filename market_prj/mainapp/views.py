from django.shortcuts import render
from django.contrib import auth
import uuid
import aldjemy
# from market_prj.market_prj.authapp import models
from authapp.models import TravelUser,TravelUserProfile,UserCaseProfile
import authapp
def main(request):
    return render(request, 'mainapp/index.html')

# Create your views here.

from .models import Accommodation
def accommodations(request):
    title = 'размещение'
    format = 'icons'
    curent_user = auth.get_user(request)
    profile_curr_user = TravelUserProfile.objects.filter(user=curent_user.id)
    # print(list(profile_curr_user.values('accomm_format')),curent_user.id)
    curr_profile =  profile_curr_user.values('accomm_format')
    if curr_profile:
        format = curr_profile[0]['accomm_format']
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('btn_format'):
            # print('1')
            # format = request.POST.get('format')
            if format == 'table':
                format = 'icons'
            elif format == 'icons':
                format = 'table'
        elif request.POST.get('btnс'):
            btnc_id = request.POST.get('btnс')
            UserCaseProfile.update_user_countryes(userid=curent_user.id, countryid=btnc_id)

        TravelUserProfile.objects.filter(user=curent_user.id).update(accomm_format=format)
        # print(btn_format)
    # list_of_accommodations = Accommodation.objects.filter(is_active=True)
    list_of_accommodations = Accommodation.get_country_items(None,'country')
    list_of_country = ListOfCountries.objects.values('id','name')
    # for a in list_of_accommodations:
    #     print('accomm=',a.name,a.region,a.region.country)

    content = {
        'title': title,
        'list_of_accommodations': list_of_accommodations,
        'list_of_country': list_of_country,
        'format': format,
    }

    return render(request, 'mainapp/accommodations.html', content)

from django.shortcuts import get_object_or_404
from .models import ListOfCountries

def accommodation(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'accommodation': get_object_or_404(Accommodation, pk=pk),
    }

    return render(request, 'mainapp/accommodation_details.html', content)
