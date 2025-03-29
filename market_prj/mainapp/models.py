import uuid
# Create your models here.
# from django.conf import settings

from django.db import models
import authapp
class ListOfCountries(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

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
        reslt = Accommodation.objects.filter(is_active=True).order_by('country','regions','name')
        return reslt

    @staticmethod
    def get_country_items(country_id, join_type):
        # list_of_accommodations = Accommodation.sa.query()
        # list_of_accommodations1 = list_of_accommodations.join(Regions.sa,Accommodation.sa.region.has(Regions.sa.id))
        # list_of_accommodations2 = list_of_accommodations1.filter(Regions.sa.country.has(uuid.UUID(country_id))).all()
        # # list_of_accommodations2 = list_of_accommodations1.filter(Regions.sa.country.has(uuid(country_id)))
        list_of_accommodations2 = Accommodation.objects.select_related('region')
        if join_type=='country':
            list_of_accommodations2 = list_of_accommodations2.select_related('country')
        if isinstance(country_id,list):
            # country_id1 = ( uuid.UUID(cnt_id) for cnt_id in country_id)
            print('country_id(list)=', country_id)
            list_of_accommodations2 = list_of_accommodations2.filter(region_id__country_id__in=country_id)

        elif country_id:
            list_of_accommodations2 = list_of_accommodations2.filter(region_id__country_id=uuid.UUID(country_id))
            # list_of_accommodations2.filter(country_id=country_id)
            print('country_id()=',uuid.UUID(country_id))
            print(list_of_accommodations2.values('region_id__country_id'))
            # list_of_accommodations2 = list_of_accommodations2.values('name','region','price','region_id__country_id__name')
            # print(list_of_accommodations2.values('region_id__country_id__name'))

        list_of_accommodations2 = list_of_accommodations2.order_by('name')
        # print('la= ',list_of_accommodations2[0])
        return list_of_accommodations2


    def __str__(self):
        return f'{self.name} ({self.country.name})'
