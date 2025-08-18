# farmers/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def sum_total(items, attr):
    return sum(getattr(i, attr)() for i in items)
