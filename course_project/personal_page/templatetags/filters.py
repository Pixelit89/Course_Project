from django import template
from django.template.defaultfilters import stringfilter
from ..models import Account

register = template.Library()


@register.filter
@stringfilter
def cut_news(value):
    max_length = 300
    try:
        assert len(value) >= 300
        return '{}...'.format(value[:max_length])
    except AssertionError:
        return value


@register.filter
def get_author(value):
    obj = Account.objects.get(id=value)
    name = obj.first_name
    surname = obj.last_name
    return '{0} {1}'.format(name, surname)