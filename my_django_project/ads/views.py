from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Ad, Request
from django.views.decorators.http import require_POST
from .forms import AdForm, RequestForm
from django.utils.text import slugify
import uuid
from .models import Category
from .forms import TagForm
from .models import Tag
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse

def requests_list(request):
    return HttpResponse("Это страница запросов.")

@login_required
@require_POST
def toggle_bookmark(request):
    ad_slug = request.POST.get('ad_slug')
    ad = get_object_or_404(Ad, slug=ad_slug)

    if request.user in ad.bookmarks.all():
        ad.bookmarks.remove(request.user)
        status = 'removed'
    else:
        ad.bookmarks.add(request.user)
        status = 'added'

    return JsonResponse({'status': status})

def main_page(request):
    ads_list = Ad.objects.all().order_by('-created_at')  # или ваш фильтр
    paginator = Paginator(ads_list, 10)  # 10 объявлений на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    context = {
        'ads': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'ads/templates/ads/ad_list.html', context)
# Список всех объявлений
def ad_list(request):
    query = request.GET.get('q', '')  # Получаем строку поиска из GET
    ads = Ad.objects.all()

    if query:
        # Поиск по названию и описанию (пример)
        ads = ads.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    ads = ads.order_by('-created_at')
    paginator = Paginator(ads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()

    # Формируем строку GET-параметров без параметра page для пагинации
    get_params = request.GET.copy()
    if 'page' in get_params:
        get_params.pop('page')

    context = {
        'ads': page_obj.object_list,
        'categories': categories,
        'page_obj': page_obj,
        'search_query': query,
        'get_params': get_params.urlencode(),  # это мы будем добавлять в ссылки пагинации
    }
    return render(request, 'ads/ad_list.html', context)

# Детальный просмотр объявления
def ad_detail(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    ad.views = ad.views + 1
    ad.save(update_fields=['views'])
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