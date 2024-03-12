from .models import Baza
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea


class BazaForm(ModelForm):
    class Meta:
        model=Baza
        fields = ['group', 'comments', 'text', 'date']

        widgets = {
            "group": TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Номер группы'
            }),
            "comments": TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Комментарий к предмету'
            }),
            "date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder':'Дата написания'
            }),
            "text": Textarea(attrs={
                'class': 'form-control',
                'placeholder':'Комментарий'
            }),
        }