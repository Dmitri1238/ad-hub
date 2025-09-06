from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('create/', views.ad_create, name='ad_create'),  # Создание объявления
    path('my/', views.my_ads, name='my_ads'),  # Мои объявления (текущего пользователя)
    path('category/<slug:slug>/', views.ads_by_category, name='ads_by_category'),

    path('<slug:slug>/edit/', views.ad_edit, name='ad_edit'),  # Редактирование объявления
    path('<slug:slug>/delete/', views.ad_delete, name='ad_delete'),  # Удаление объявления
    path('<slug:slug>/apply/', views.send_request, name='send_request'),  # Отклик на объявление
    path('<slug:slug>/requests/', views.view_requests_for_ad, name='view_requests_for_ad'),  # Просмотр откликов

    path('<slug:slug>/', views.ad_detail, name='ad_detail'),  # Детали объявления — последний путь
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/add/', views.add_tag, name='add_tag'),
    path('ads/tag/<slug:slug>/', views.ads_by_tag, name='ads_by_tag'),
]