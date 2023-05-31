from django import template

register = template.Library()

@register.filter
def remainder(value, arg):
    try:
        return int(value)%int(arg) if (int(value)%int(arg) != 0) else False
    except (ValueError, ZeroDivisionError):
        return None