from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='accounts_index'),  # например, страница аккаунта
    path('register/', views.register, name='register'),  # регистрация
]