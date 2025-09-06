from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Ad, Request
from .forms import AdForm, RequestForm
from django.utils.text import slugify
import uuid
from .models import Category
from .forms import TagForm
from django.contrib.auth.decorators import login_required
from .models import Tag


# Список всех объявлений
def ad_list(request):
    ads = Ad.objects.all()
    categories = Category.objects.all()
    return render(request, 'ads/ad_list.html', {'ads': ads, 'categories': categories})

# Детальный просмотр объявления
def ad_detail(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

# Создание объявления (только для авторизованных)
@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user

            # Генерируем уникальный slug, если его еще нет
            if not ad.slug:
                ad.slug = generate_unique_slug(ad)

            ad.save()
            return redirect('ad_detail', slug=ad.slug)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})

def generate_unique_slug(instance):
    slug_base = slugify(instance.title)
    slug = slug_base
    while Ad.objects.filter(slug=slug).exists():
        slug = f"{slug_base}-{uuid.uuid4().hex[:8]}"
    return slug

# Редактирование объявления (только для автора)
@login_required
def ad_edit(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    if request.user != ad.author:
        return HttpResponseForbidden("Вы не можете редактировать это объявление.")
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', slug=ad.slug)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_edit.html', {'form': form, 'ad': ad})

# Удаление объявления (только для автора)
@login_required
def ad_delete(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    if request.user != ad.author:
        return HttpResponseForbidden("Вы не можете удалять это объявление.")
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})

# Мои объявления
@login_required
def my_ads(request):
    ads = Ad.objects.filter(author=request.user)
    return render(request, 'ads/my_ads.html', {'ads': ads})

# Отправка заявки на объявление
@login_required
def send_request(request, slug):
    ad = get_object_or_404(Ad, slug=slug)

    # Проверка: нельзя откликаться на своё объявление
    if request.user == ad.author:
        return redirect('ad_detail', slug=ad.slug)

    if request.method == 'POST':
        # Создаём заявку
        Request.objects.create(
            ad=ad,
            sender=request.user,
            recipient=ad.author,
            status='new'
        )
        return redirect('ad_detail', slug=ad.slug)
    return render(request, 'ads/send_request.html', {'ad': ad})

# Просмотр заявок для объявления (только для автора)
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

    categories = Category.objects.all()  # чтобы передать в шаблон список категорий

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
            return redirect('ad_list')  # или куда хотите после создания
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