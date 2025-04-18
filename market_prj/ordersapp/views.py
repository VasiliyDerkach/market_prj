from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from decimal import Decimal
from django.urls import reverse
from django.urls import reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from basketapp.models import Basket
from ordersapp.models import Order
from ordersapp.models import OrderItem
from ordersapp.forms import OrderItemForm
from mainapp.models import Apartmen
from django.template.loader import render_to_string
from django.http import JsonResponse

# список заказов
class OrderList(ListView):
    model = Order

    def get_queryset(self):
        order_items = Order.objects.filter(user=self.request.user)
        return order_items


# создание заказа с товарными позициями
class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1, fields='__all__')
        sumprice = 0
        sumnights = 0

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.get_items(self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order,
                                                     OrderItem,
                                                     form=OrderItemForm,
                                                     extra=len(basket_items),
                                                     fields='__all__')
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.fields['apartmen'].queryset = Apartmen.objects.filter(accommodation=basket_items[num].accommodation)
                    form.initial['accommodation'] = basket_items[num].accommodation
                    form.fields['apartmen'].queryset = Apartmen.objects.filter(accommodation_id=basket_items[num].accommodation_id)
                    form.initial['apartmen'] = basket_items[num].apartmen
                    form.initial['nights'] = basket_items[num].nights
                    sumnights += form.initial['nights']
                    if basket_items[num].apartmen:
                        price_apart = 1+basket_items[num].apartmen.price/100
                        form.initial['price_order'] = (basket_items[num].accommodation.price * price_apart).quantize(Decimal("1.00"))
                    else:
                        form.initial['price_order'] = basket_items[num].accommodation.price
                    sprice = form.initial['price_order'] * form.initial['nights']
                    form.initial['price'] = sprice
                    sumprice += sprice
                    # print('form.fields.=', dir(form.fields['apartmen'].prepare_value))
                basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        data['sumprice'] = sumprice
        data['sumnights'] = sumnights
        data['user'] = self.request.user

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


# редактирование заказа с товарными позициями
class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order,
                                             OrderItem,
                                             form=OrderItemForm,
                                             extra=1,
                                             fields='__all__')
        formset = OrderFormSet()
        for num, form in enumerate(formset.forms):
            form.fields['apartmen'].queryset = Apartmen.objects.filter(accommodation_id=form.fields['accommodation_id'])
            print('form.fields=',dir(form.fields['apartmen']))

        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            data['orderitems'] = OrderFormSet(instance=self.object)
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.price_order
            data['orderitems'] = formset

        return data


# карточка заказа
class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


# удаление заказа
class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))

# @login_required
# def orderitem_edit(request, pk, nights):
#     if request.is_ajax():
#         nights = int(nights)
#         new_orderitem_item = OrderItem.objects.filter(id=pk).get()
#         if nights > 0:
#             new_orderitem_item.nights = nights
#             new_orderitem_item.save()
#         else:
#             new_orderitem_item.delete()
#         order_items = OrderItem.objects.filter(user=request.user,order=new_orderitem_item.order)
#         # .order_by(
#         #     'accommodation__region_id__country_id')
#         content = {
#             'basket_items': order_items,
#         }
#         result = render_to_string('ordersapp/order_form.html',
#                                   content)
#         return JsonResponse({'result': result})
