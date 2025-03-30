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

from .models import Accommodation, Regions, ListOfCountries
def accommodations(request):
    title = 'размещение'
    format = 'icons'
    type_param = None
    cnt_case = []
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
        if request.POST.get('btnс') and curent_user:
            btnc_id = request.POST.get('btnс')
            type_param = 'country'
            UserCaseProfile.update_user_countryes(userid=curent_user.id, countryid=btnc_id)
        if request.POST.get('btnr') and curent_user:
            btnr_id = request.POST.get('btnr')
            type_param = 'region'
            UserCaseProfile.update_user_parametrs(userid=curent_user.id,parametrid= btnr_id,param_type='region')
        if request.POST.get('btn_country_clear') and curent_user:
            print('free country')
            type_param = 'country'
            UserCaseProfile.update_user_countryes(userid=curent_user.id, countryid='free')
        if (request.POST.get('btnс') or request.POST.get('btn_countryes')) and curent_user:
            print('btn2')
            type_param = 'country'
            cnt_case = list(UserCaseProfile.objects.filter(user_id=curent_user.id,context='country').values_list('param_id',flat=True))
        if request.POST.get('btn_region_clear') and curent_user:
            print('free region')
            type_param = 'region'
            UserCaseProfile.update_user_parametrs(userid=curent_user.id, countryid='free',param_type='region')
            # get_regions_of_countryes
        if request.POST.get('btnr_of_countryes') and curent_user:
            type_param = 'region'
            countryes_case1 = list(
                UserCaseProfile.objects.filter(user_id=curent_user.id, context='country').values_list('param_id',
                                                                                                  flat=True))
                cnt_case = Regions.get_regions_of_countryes(countryes_case1)
        if (request.POST.get('btnr') or request.POST.get('btn_regions')) and curent_user:
            print('btnr')
            type_param = 'region'
            countryes_case0 = list(UserCaseProfile.objects.filter(user_id=curent_user.id,context='region').values_list('param_id',flat=True))

        TravelUserProfile.objects.filter(user_id=curent_user.id).update(accomm_format=format)
        # print(btn_format)
    # list_of_accommodations = Accommodation.objects.filter(is_active=True)
    print('countryes_case=', cnt_case)
    # list_of_accommodations = Accommodation.get_country_items(countryes_case,'country')
    list_of_accommodations = Accommodation.get_parametrs_items( cnt_case, type_param,'country')
    # list_of_accommodations = Accommodation.get_country_items('00000000-0000-0000-0000-000000000003','country')
    list_of_country = ListOfCountries.objects.values('id','name')
    List_of_regions = Regions.objects.values('id','name')
    for elm in list_of_country:
        # print(elm['id'])
        if UserCaseProfile.objects.filter(user_id=curent_user.id, param_id=elm['id'], context='country'):
            elm['is_active'] = True
        else:
            elm['is_active'] = False
    for elm in List_of_regions:
        # print(elm['id'])
        if UserCaseProfile.objects.filter(user_id=curent_user.id, param_id=elm['id'], context='region'):
            elm['is_active'] = True
        else:
            elm['is_active'] = False
    # for a in list_of_accommodations:
    #     print('accomm=',a.name,a.region,a.region.country)

    content = {
        'title': title,
        'list_of_accommodations': list_of_accommodations,
        'list_of_country': list_of_country,
        'list_of_regions': List_of_regions,
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
