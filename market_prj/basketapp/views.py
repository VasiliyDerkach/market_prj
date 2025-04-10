from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from basketapp.models import Basket
from mainapp.models import Accommodation, Apartmen


# отображение списка записей корзины
@login_required
def basket(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(
        user=request.user).order_by('accommodation__region_id__country_id')
    for itm in basket_items:
        print(itm)
        if itm.apartmen:
            itm.price_plus = int(itm.accommodation.price*(1+itm.apartmen.price/100))
        else:
            itm.price_plus = itm.accommodation.price
    content = {
        'title': title,
        'basket_items': basket_items,
    }

    return render(request, 'basketapp/basket.html', content)

# добавление продукта в корзину
@login_required
def basket_add(request, pk):

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('acc:accommodations', args=[pk]))

    accommodation = get_object_or_404(Accommodation, pk=pk)
    basket = Basket.objects.filter(user=request.user,
                                   accommodation=accommodation).first()
    # list_apartmen = Apartmen.get_accommodation_items(pk)

    if not basket:
        basket = Basket(user=request.user, accommodation=accommodation, country_id=accommodation.region.country_id)

    basket.nights += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# удаление продукта из корзины
@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, nights):
    print("привет pk = ",pk)
    if request.is_ajax():
        nights = int(nights)
        # new_basket_item = Basket.objects.get(pk)
        new_basket_item = Basket.objects.filter(id=pk).get()
        print('Basket.objects.get(pk)=',new_basket_item)
        if nights > 0:
            new_basket_item.nights = nights
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by(
            'accommodation__region_id__country_id')

        content = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html',
                                  content)

        return JsonResponse({'result': result})
