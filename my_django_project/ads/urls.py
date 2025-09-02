from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('slug:<slug:slug>/', views.ad_detail, name='ad_detail'),
    path('create/', views.ad_create, name='ad_create'),
    path('<slug:slug>/edit/', views.ad_edit, name='ad_edit'),
    path('<slug:slug>/delete/', views.ad_delete, name='ad_delete'),
    path('my/', views.my_ads, name='my_ads'),
    path('<slug:ad_slug>/apply/', views.send_request, name='send_request'),
    path('<slug:ad_slug>/requests/', views.view_requests_for_ad, name='view_requests_for_ad'),
]