from django import forms
from .models import Ad, Category

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
        fields = ['title', 'description', 'price', 'city', 'category']
        
class RequestForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()