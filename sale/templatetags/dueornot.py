from django.template import Library
import datetime

register = Library()

@register.filter
def dueornot(bill_date):
    # return type(bill_date)
    present_date = datetime.datetime.now(datetime.timezone.utc)
    # print('\n$$$$$$', (present_date-bill_date).days)
    return (present_date-bill_date).days >= 1
    # return ((((present_date-bill_date).seconds)/60)/60)