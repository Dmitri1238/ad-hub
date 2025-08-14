from django.urls import path
from . import views

urlpatterns = [
    # Список всех объявлений
    path('', views.ad_list, name='ad_list'),

    # Детальный просмотр объявления
    path('<int:pk>/', views.ad_detail, name='ad_detail'),

    # Создание объявления (только для авторизованных)
    path('create/', views.ad_create, name='ad_create'),

    # Редактирование объявления (только для автора)
    path('<int:pk>/edit/', views.ad_edit, name='ad_edit'),

    # Удаление объявления (только для автора)
    path('<int:pk>/delete/', views.ad_delete, name='ad_delete'),

    # Мои объявления
    path('my/', views.my_ads, name='my_ads'),

    # Откликнуться на объявление (отправить заявку)
    path('<int:ad_pk>/apply/', views.send_request, name='send_request'),

    # Просмотр откликов на свои объявления (для автора)
    path('<int:ad_pk>/requests/', views.view_requests_for_ad, name='view_requests_for_ad'),
    
]