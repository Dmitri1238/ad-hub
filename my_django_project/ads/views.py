from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Ad, Request
from .forms import AdForm, RequestForm

# Список всех объявлений
def ad_list(request):
    ads = Ad.objects.all()
    return render(request, 'ads/ad_list.html', {'ads': ads})

# Детальный просмотр объявления
def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

# Создание объявления (только для авторизованных)
@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})

# Редактирование объявления (только для автора)
@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            # замените 'ad_detail' на актуальное имя вашего маршрута
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_edit.html', {'form': form})

# Удаление объявления (только для автора)
@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
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
def send_request(request, ad_pk):
    ad = get_object_or_404(Ad, pk=ad_pk)

    # Проверка: нельзя откликаться на своё объявление
    if request.user == ad.author:
        # Можно показать сообщение или просто редирект
        return redirect('ad_detail', pk=ad_pk)

    if request.method == 'POST':
        # Создаём заявку
        Request.objects.create(
            ad=ad,
            sender=request.user,
            recipient=ad.author,
            status='new'
        )
        # Можно добавить сообщение об успехе (через messages)
        return redirect('ad_detail', pk=ad_pk)
    return render(request, 'ads/send_request.html', {'ad': ad})

@login_required
def view_requests_for_ad(request, ad_pk):
    ad = get_object_or_404(Ad, pk=ad_pk)
    # Проверка, что текущий пользователь — автор объявления
    if request.user != ad.author:
        return HttpResponseForbidden("У вас нет доступа к заявкам этого объявления.")
    requests = Request.objects.filter(ad=ad)
    return render(request, 'ads/view_requests.html', {'ad': ad, 'requests': requests})

