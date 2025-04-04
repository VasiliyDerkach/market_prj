from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
import uuid

class TravelUser(AbstractUser):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)


class TravelUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        TravelUser, unique=True, null=False, db_index=True,
        on_delete=models.CASCADE)
    tagline = models.CharField(
        verbose_name='теги', max_length=128, blank=True)
    aboutMe = models.TextField(
        verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(
        verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    accomm_format = models.CharField(
        verbose_name='формат показа путевок', max_length=70, blank=None, default='icons')
    @receiver(post_save, sender=TravelUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            TravelUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=TravelUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.traveluserprofile.save()

class UserCaseProfile(models.Model):
    user = models.ForeignKey(TravelUser, on_delete=models.CASCADE)
    param_id = models.UUIDField(
        verbose_name='id параметра профиля',  blank=False)
    context = models.CharField(
        verbose_name='контекст параметра', max_length=128, blank=True)

    @staticmethod
    def update_user_countryes(userid, countryid):
        print(userid, countryid)
        if countryid=='free':
            UserCaseProfile.objects.filter(user_id=userid, context='country').delete()
        else:
            if UserCaseProfile.objects.filter(user_id=userid,param_id=countryid):
                UserCaseProfile.objects.filter(user_id=userid, param_id=countryid, context='country').delete()
            else:
                UserCaseProfile.objects.create(user_id=userid, param_id=countryid,context='country')

    @staticmethod
    def update_user_parametrs(userid, parametrid,param_type):
        print(userid, parametrid)
        is_check = False
        if parametrid=='free':
            UserCaseProfile.objects.filter(user_id=userid,context=param_type).delete()
        else:
            if not isinstance(parametrid,list) and parametrid:
                parametrid = [parametrid]
                is_check = True
            if parametrid:
                for p in parametrid:
                    incase = UserCaseProfile.objects.filter(user_id=userid, param_id=p, context=param_type)
                    if incase and is_check:
                        incase.delete()
                    else:
                        if not incase:
                            UserCaseProfile.objects.create(user_id=userid, param_id=p,context=param_type)
