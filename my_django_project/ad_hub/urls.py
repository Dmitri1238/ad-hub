from django.contrib import admin
from django.urls import path, include
import ads.views as ads_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Аутентификация (вход/выход/смена пароля)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Регистрация и профиль — внутри приложения accounts
    path('accounts/', include('accounts.urls')),  # предполагается, что в accounts/urls.py есть маршруты для регистрации и профиля
    
    # Объявления
    path('ads/', include('ads.urls')),
    
    # Отклики
    path('requests/', ads_views.requests_list, name='requests_list'),
]