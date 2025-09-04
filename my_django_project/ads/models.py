from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField("Название категории", max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Ad(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    city = models.CharField("Город", max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name="Автор"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ads',
        verbose_name="Категория"
    )
    slug = models.SlugField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('ad_detail', kwargs={'slug': self.slug})

class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
    ]

    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='requests',
        verbose_name="Объявление"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_requests',
        verbose_name="Отправитель"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_requests',
        verbose_name="Получатель"
    )
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Запрос от {self.sender} к {self.recipient} по объявлению {self.ad}"