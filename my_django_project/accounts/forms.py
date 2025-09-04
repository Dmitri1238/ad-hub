from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(username=username, password=password)
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')