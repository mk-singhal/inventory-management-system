from django.template import Library

register = Library()

@register.filter
def index(List, i):
    return List[int(i)]