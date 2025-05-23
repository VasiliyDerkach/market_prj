import uuid
# Create your models here.
# from django.conf import settings

from django.db import models
import authapp
class PartsOfWorld(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name
class ListOfCountries(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)
    partsofworld = models.ForeignKey(PartsOfWorld, on_delete=models.CASCADE,blank=True,default=None,null=True)
    def __str__(self):
        return self.name

class Regions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.ForeignKey(ListOfCountries, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name
    @staticmethod
    def get_regions_of_countryes(lst_countryes):
        return Regions.objects.filter(country_id__in=lst_countryes)
class Accommodation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.ForeignKey(ListOfCountries, on_delete=models.CASCADE)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, related_name='Regionid')
    name = models.CharField(verbose_name='название проживания',
                                           max_length=128, unique=True)
    image = models.ImageField(upload_to='accommodation_img', blank=True)
    short_desc = models.TextField(verbose_name='краткое описание продукта',
                                  max_length=60, blank=True)
    description = models.TextField(verbose_name='описание продукта',
                                   blank=True)
    availability = models.PositiveIntegerField(
				verbose_name='количество свободных номеров')
    price = models.DecimalField(
        verbose_name='цена', max_digits=8, decimal_places=2, default=0)
    room_desc = models.TextField(verbose_name='краткое описание комнаты',
                                 max_length=60, blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    @staticmethod
    def get_items():
        reslt = Accommodation.objects.filter(is_active=True).order_by('region_id__country_id','regions','name')
        return reslt

    @staticmethod
    def get_country_items(country_id, join_type):
        list_of_accommodations2 = Accommodation.objects.select_related('region')
        if join_type=='country':
            list_of_accommodations2 = list_of_accommodations2.select_related('country')
        if isinstance(country_id,list):
            # print('country_id(list)=', country_id)
            list_of_accommodations2 = list_of_accommodations2.filter(region_id__country_id__in=country_id)

        elif country_id:
            list_of_accommodations2 = list_of_accommodations2.filter(region_id__country_id=uuid.UUID(country_id))

        list_of_accommodations2 = list_of_accommodations2.order_by('region_id__country_id','region_id','name')
        return list_of_accommodations2

    @staticmethod
    def get_parametrs_items(param_id,param_type, join_type):
        list_of_accommodations2 = Accommodation.objects.select_related('region')
        if join_type == 'country':
            list_of_accommodations2 = list_of_accommodations2.select_related('country')
        if isinstance(param_id, list):
            print('param_id(list)=', param_id)
            if param_type=='country':
                list_of_accommodations2 = list_of_accommodations2.filter(region_id__country_id__in=param_id)
            elif param_type=='region':
                list_of_accommodations2 = list_of_accommodations2.filter(region_id__in=param_id)
        elif param_id:
            if param_type=='country':
                list_of_accommodations2 = list_of_accommodations2.filter(region_id__country_id=uuid.UUID(param_id))
            elif param_type == 'region':
                list_of_accommodations2 = list_of_accommodations2.filter(region_id=uuid.UUID(param_id))
            print('param_id()=', uuid.UUID(param_id))
        list_of_accommodations2 = list_of_accommodations2.order_by('region_id__country_id', 'region_id', 'name')
        return list_of_accommodations2

    def __str__(self):
        return f'{self.name} ({self.country.name})'
class Apartmen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='название типа номеров',
                                           max_length=128, unique=True)
    image = models.ImageField(upload_to='apartmen_img', blank=True,default=None)
    short_desc = models.TextField(verbose_name='краткое описание типа номеров',
                                  max_length=60, blank=True,default=None)
    description = models.TextField(verbose_name='описание типа номеров',
                                   blank=True,default=None)
    availability = models.PositiveIntegerField(
				verbose_name='количество свободных номеров',default=None)
    price = models.DecimalField(
        verbose_name='цена % об базового тарифа', max_digits=8, decimal_places=2, default=0)

    @staticmethod
    def get_accommodation_items(accommodation):
        return Apartmen.objects.filter(accommodation=accommodation)
    def __str__(self):
        return f'{self.name} ({self.accommodation.name})'
