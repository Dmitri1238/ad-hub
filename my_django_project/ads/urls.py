from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),  # Страница со списком объявлений
    path('create/', views.ad_create, name='ad_create'),
    path('my/', views.my_ads, name='my_ads'),
    path('category/<slug:slug>/', views.ads_by_category, name='ads_by_category'),
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/add/', views.add_tag, name='add_tag'),
    path('tag/<slug:slug>/', views.ads_by_tag, name='ads_by_tag'),
    
    # Маршрут для установки темы (например, theme1, theme2, theme3)
    path('set_theme/<str:theme_name>/', views.set_theme, name='set_theme'),
    path('change_theme/<str:theme>/', views.change_theme, name='change_theme'),
    
    # Остальные маршруты, отвечающие за конкретные действия:
    path('<slug:slug>/toggle_bookmark/', views.toggle_bookmark, name='toggle-bookmark-slug'),  
    path('<slug:slug>/edit/', views.ad_edit, name='ad_edit'),
    path('<slug:slug>/delete/', views.ad_delete, name='ad_delete'),
    path('<slug:slug>/apply/', views.send_request, name='send_request'),
    path('<slug:slug>/requests/', views.view_requests_for_ad, name='view_requests_for_ad'),
    path('<slug:slug>/add_review/', views.add_review, name='add_review'),

    # Деталь объявления — последний маршрут:
    path('<slug:slug>/', views.ad_detail, name='ad_detail'),
]