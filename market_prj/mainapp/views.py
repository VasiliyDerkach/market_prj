from django.shortcuts import render
from django.contrib import auth
from authapp.models import TravelUser,TravelUserProfile,UserCaseProfile
import authapp
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from mainapp.models import Apartmen
from basketapp.models import Basket
def main(request):
    return render(request, 'mainapp/index.html')

# Create your views here.

from .models import Accommodation, Regions, ListOfCountries
def accommodations(request):
    title = 'размещение'
    format = 'icons'
    typeparam = None
    cntcase = None
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
            typeparam = 'country'
            UserCaseProfile.update_user_countryes(userid=curent_user.id, countryid=btnc_id)
        if request.POST.get('btnr') and curent_user:
            btnr_id = request.POST.get('btnr')
            typeparam = 'region'
            UserCaseProfile.update_user_parametrs(userid=curent_user.id,parametrid= btnr_id,param_type='region')
        if request.POST.get('btn_country_clear') and curent_user:
            print('free country')
            typeparam = 'country'
            UserCaseProfile.update_user_countryes(userid=curent_user.id, countryid='free')
        if (request.POST.get('btnс') or request.POST.get('btn_countryes')) and curent_user:
            print('btn2')
            typeparam = 'country'
            cntcase = list(UserCaseProfile.objects.filter(user_id=curent_user.id,context='country').values_list('param_id',flat=True))
        if request.POST.get('btn_region_clear') and curent_user:
            print('free region')
            typeparam = 'region'
            UserCaseProfile.update_user_parametrs(userid=curent_user.id, parametrid='free',param_type='region')
            # get_regions_of_countryes
        if request.POST.get('btnr_of_countryes') and curent_user:
            typeparam = 'region'
            countryes_case1 = list(UserCaseProfile.objects.filter(user_id=curent_user.id, context='country').values_list('param_id',flat=True))
            print('countryes_case1=',countryes_case1)
            cntcase = list(Regions.get_regions_of_countryes(countryes_case1).values_list('id',flat=True))
            UserCaseProfile.update_user_parametrs(userid=curent_user.id, parametrid=cntcase, param_type='region')
        if (request.POST.get('btnr') or request.POST.get('btn_regions')) and curent_user:
            print('btnr')
            typeparam = 'region'
            cntcase = list(UserCaseProfile.objects.filter(user_id=curent_user.id,context='region').values_list('param_id',flat=True))

        TravelUserProfile.objects.filter(user_id=curent_user.id).update(accomm_format=format)
        # print(btn_format)
    # list_of_accommodations = Accommodation.objects.filter(is_active=True)
    print('countryes_case=', cntcase)
    # list_of_accommodations = Accommodation.get_country_items(countryes_case,'country')
    list_of_accommodations = Accommodation.get_parametrs_items(param_id=cntcase, param_type=typeparam, join_type='country')
    # list_of_accommodations = Accommodation.get_country_items('00000000-0000-0000-0000-000000000003','country')
    list_of_country = ListOfCountries.objects.values('id','name')
    List_of_regions = Regions.objects.select_related('country').values('id','name','country_id','country_id__name')
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
    pagename = 'accommodations'
    content = {
        'title': title,
        'pagename': pagename,
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
    list_apartmen = Apartmen.get_accommodation_items(pk)
    if request.method == 'POST':
        if request.POST.get('btn_accom_add'):
            val = request.POST.getlist('radio_app')
            if val:
                for elm in list_apartmen:
                    if str(elm.id) in list(val):
                        basket = Basket.objects.filter(user=request.user,accommodation_id=pk,apartmen_id=str(elm)).first()
                        if not basket:
                            basket = Basket(user=request.user, accommodation=accommodation,
                                            country_id=accommodation.region.country_id,apartmen_id=idap)

                        basket.nights += 1
                        basket.save()

    content = {
        'title': title,
        'accommodation': get_object_or_404(Accommodation, pk=pk),
        'list_apartmen': list_apartmen,
    }
    # print('request=',request)
    return render(request, 'mainapp/accommodation_details.html', content)

class ApartmenList(ListView):
    model = Apartmen
    def get_queryset(self):
        print('self.request=', self.request)
        return Apartmen.objects.filter( accommodation_id=self.request.accommodation_id)
