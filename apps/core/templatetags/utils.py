import pytz
from django import template
from django.conf import settings
from persiantools.digits import to_word
from persiantools.jdatetime import JalaliDateTime

register = template.Library()


@register.filter
def jdate(value, fmt):
    """ Format a date in jalali date according to the given format. """
    datetime = value.astimezone(pytz.timezone(settings.TIME_ZONE))
    return JalaliDateTime.to_jalali(
        year=datetime.year,
        month=datetime.month,
        day=datetime.day,
        hour=datetime.hour,
        minute=datetime.minute,
        second=datetime.second,
        microsecond=datetime.microsecond,
    ).strftime(fmt)


@register.filter
def digit_to_word(digit):
    """ Get a digit and convert it to persian word. """
    return to_word(digit)


@register.inclusion_tag('ordering.html')
def ordering(model, *attrs):
    """
    Ordering inclusion tag to make ordering action based on model and given attrs.

    The model class will get from first index of `object_list` context.
    If the attr starts with `-`, the ordering will be descending.
    """
    cls = model.__class__
    fields = []
    for attr in attrs:
        desc = False
        if attr.startswith('-'):
            desc = True
            attr = attr[1:]
        field = getattr(cls, attr).field
        fields.append({'field_cls': field, 'desc': desc})

    return {
        'fields': fields
    }
