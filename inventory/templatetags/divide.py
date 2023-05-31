from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return int(int(value) / int(arg))
    except (ValueError, ZeroDivisionError):
        return None