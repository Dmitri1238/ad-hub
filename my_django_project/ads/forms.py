from django import forms
from .models import Ad, Category
from .models import Tag

class AdForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(name__in=[
            "Недвижимость",
            "Квартиры",
            "Транспорт",
            "Легковые автомобили",
            "Вакансии",
            "Резюме",
            "Товары",
            "Продажа животных",
        ]),
        empty_label="Выберите категорию",
        widget=forms.Select()
    )

    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'city', 'category', 'tags']
        
class RequestForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

class TagForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        label="Название тега",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название тега',
            'autocomplete': 'off',
        }),
        help_text="Введите уникальное название тега (до 50 символов)."
    )

    class Meta:
        model = Tag
        fields = ['name']