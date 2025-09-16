# ads/templatetags/my_filters.py
from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def local_time(value, format_string="N j, Y, P"):
    if not value:
        return ""
    # Преобразует дату и возвращает строку в нужном формате
    local_dt = timezone.localtime(value)
    return local_dt.strftime(format_string)