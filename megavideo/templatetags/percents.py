from django.template import Library
from django.template import Context, Template

register = Library()

def percent_calc(total, value):
    try:
        per = '%.2f' % (float((int(total) + 0.0) / int(value)) * 100)
    except:
        per = '0.0'
    return per

@register.filter
def percent(value, total):
    return percent_calc(value, total)
