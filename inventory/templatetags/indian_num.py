from django.template import Library
from babel.numbers import format_currency

register = Library()

@register.filter
def indian_num(num):
    return format_currency(num, 'INR', locale='en_IN')
    # return List[int(i)]