from django import forms
from ordersapp.models import Order
from ordersapp.models import OrderItem
from mainapp.models import Accommodation,Apartmen


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    model = OrderItem
    price = forms.CharField(label='цена', required=False,widget=forms.TextInput(attrs={'readonly':'readonly'}))
    exclude = ()

    def __init__(self,  *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
