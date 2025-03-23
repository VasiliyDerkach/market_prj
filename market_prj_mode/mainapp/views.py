from django.shortcuts import render
# импортируем auth для получения доступа к данным текущего пользователя из модуля mainapp
from django.contrib import auth
# импортируем модели из authapp, чтобы работать с данными профиля текущего пользвателя
from authapp.models import TravelUser,TravelUserProfile

def main(request):
    return render(request, 'mainapp/index.html')

# Create your views here.

from .models import Accommodation
def accommodations(request):
    title = 'размещение'
    # format - переменная,отвечающая за формат, выбранный текущим пользователем, для отображения списка путевок 
	#(с картинкой значение icons по умолчанию, table -без них)
    format = 'icons'
    # получаем экземпляр класса данных текущего авторизовавшегося пользователя
    curent_user = auth.get_user(request)
    # получаем экземпляр класса данных профиля текущего авторизовавшегося пользователя
    profile_curr_user = TravelUserProfile.objects.filter(user=curent_user.id)
    # accomm_format - имя поля в модели TravelUserProfile отвечающее за сохранения формата списка путевок, выборанного пользователем
    # сохраняем значение поля accomm_format в переменную format
    format = profile_curr_user.values('accomm_format')[0]['accomm_format']
    if request.method == 'POST':
    # задаем значение переменной format в зависимости от нажатой в шаблоне кнопки
        if request.POST.get('btn_table'):
            format = 'table'
        if request.POST.get('btn_icons'):
            format = 'icons'
    # в модели профиля для текущего пользователя сохраняем, выбранный пользователем формат списка путевок
        TravelUserProfile.objects.filter(user=curent_user.id).update(accomm_format=format )
    list_of_accommodations = Accommodation.objects.filter(is_active=True)
    # передаем переменную format в шаблон, который отобразит списко путевок в выбранном формате
    content = {
        'title': title,
        'list_of_accommodations': list_of_accommodations,
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
