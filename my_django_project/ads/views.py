from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse, HttpResponseForbidden, JsonResponse
)
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.utils.text import slugify
from ads.models import Ad, FavoriteAd

import uuid

from .models import Ad, Request, Category, Tag
from .forms import AdForm, RequestForm, TagForm
import json


def requests_list(request):
    # Заглушка, можно потом дополнить
    return HttpResponse("Это страница запросов.")

@login_required
@require_POST
def toggle_bookmark(request, slug):
    try:
        ad = Ad.objects.get(slug=slug)
    except Ad.DoesNotExist:
        return JsonResponse({'error': 'Объявление не найдено.'}, status=404)

    favorite, created = FavoriteAd.objects.get_or_create(user=request.user, ad=ad)
    if created:
        status = 'added'
        is_favorited = True
    else:
        favorite.delete()
        status = 'removed'
        is_favorited = False

    return JsonResponse({'status': status, 'is_favorited': is_favorited})

def main_page(request):
    ads_list = Ad.objects.all().order_by('-created_at')
    paginator = Paginator(ads_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    # Получение списка избранных объявлений текущего пользователя
    if request.user.is_authenticated:
        fav_ids = FavoriteAd.objects.filter(user=request.user).values_list('ad_id', flat=True)
    else:
        fav_ids = []

    context = {
        'ads': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'favorite_ids': list(fav_ids),  # передача списка ID в шаблон
    }
    return render(request, 'ads/ad_list.html', context)


def ad_list(request):
    query = request.GET.get('q', '')  # поисковый запрос
    ads = Ad.objects.all()

    if query:
        ads = ads.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    ads = ads.order_by('-created_at')
    paginator = Paginator(ads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Создаем копию GET-параметров, исключая 'page' для построения get-запросов
    get_params = request.GET.copy()
    get_params.pop('page', None)

    context = {
        'ads': page_obj.object_list,
        'categories': Category.objects.all(),
        'page_obj': page_obj,
        'search_query': query,
        'get_params': get_params.urlencode(),
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # возвращаем только HTML для вставки
        return render(request, 'ads/_ad_items.html', context)

    # обычный ответ
    return render(request, 'ads/ad_list.html', context)


def ad_detail(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    # Увеличиваем счетчик просмотров
    ad.views = ad.views + 1
    ad.save(update_fields=['views'])
    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            if not ad.slug:
                ad.slug = generate_unique_slug(ad)
            ad.save()
            messages.success(request, "Объявление успешно создано.")
            return redirect('ad_detail', slug=ad.slug)
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})


def generate_unique_slug(instance):
    slug_base = slugify(instance.title)
    slug = slug_base
    while Ad.objects.filter(slug=slug).exists():
        slug = f"{slug_base}-{uuid.uuid4().hex[:8]}"
    return slug


@login_required
def ad_edit(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    if request.user != ad.author:
        messages.warning(request, "У вас нет прав на редактирование.")
        return HttpResponseForbidden("Вы не можете редактировать это объявление.")

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.info(request, "Объявление обновлено.")
            return redirect('ad_detail', slug=ad.slug)
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/ad_edit.html', {'form': form, 'ad': ad})


@login_required
def ad_delete(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    if request.user != ad.author:
        return HttpResponseForbidden("Вы не можете удалять это объявление.")

    if request.method == 'POST':
        ad.delete()
        messages.success(request, "Объявление удалено.")
        return redirect('ad_list')

    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})


@login_required
def my_ads(request):
    ads = Ad.objects.filter(author=request.user)
    return render(request, 'ads/my_ads.html', {'ads': ads})


@login_required
def send_request(request, slug):
    ad = get_object_or_404(Ad, slug=slug)

    # Нельзя откликаться на своё объявление
    if request.user == ad.author:
        messages.warning(request, "Вы не можете отправлять заявку на своё объявление.")
        return redirect('ad_detail', slug=ad.slug)

    if request.method == 'POST':
        # Создаем заявку на объявление
        Request.objects.create(
            ad=ad,
            sender=request.user,
            recipient=ad.author,
            status='new'
        )
        messages.success(request, "Заявка отправлена.")
        return redirect('ad_detail', slug=ad.slug)

    return render(request, 'ads/send_request.html', {'ad': ad})


@login_required
def view_requests_for_ad(request, ad_slug):
    ad = get_object_or_404(Ad, slug=ad_slug)
    if request.user != ad.author:
        return HttpResponseForbidden("У вас нет доступа к заявкам этого объявления.")

    requests = Request.objects.filter(ad=ad)
    return render(request, 'ads/view_requests.html', {'ad': ad, 'requests': requests})


def ads_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    ads = Ad.objects.filter(category=category)
    categories = Category.objects.all()

    context = {
        'ads': ads,
        'categories': categories,
        'current_category': category,
    }
    return render(request, 'ads/ad_list.html', context)


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Тег добавлен.")
            return redirect('ad_list')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = TagForm()

    return render(request, 'ads/add_tag.html', {'form': form})


@login_required
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'ads/tag_list.html', {'tags': tags})


def ads_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    ads = Ad.objects.filter(tags=tag)
    categories = Category.objects.all()

    context = {
        'ads': ads,
        'categories': categories,
        'current_tag': tag,
    }
    return render(request, 'ads/ad_list.html', context)