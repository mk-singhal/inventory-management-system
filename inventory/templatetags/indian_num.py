from django.template import Library
from babel.numbers import format_currency
import decimal

register = Library()

@register.filter
def indian_num(num, div=1):
    return format_currency(decimal.Decimal(num)/div, 'INR', locale='en_IN', decimal_quantization=False)
