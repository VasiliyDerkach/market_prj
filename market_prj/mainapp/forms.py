from django import forms
from mainapp.models import Apartmen


class ApartmenForm(forms.ModelForm):
    model = Apartmen
    is_choise = forms.BooleanField(label='Выбрано', required=False)
    exclude = ()

    def __init__(self, *args, **kwargs):
        super(Apartmen, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
