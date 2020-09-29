from money.models import Period
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.utils import timezone


def get_period():
    period_name = datetime.datetime.strftime(timezone.now(), '%B %Y')
    try:
        period = Period.objects.get(name=period_name)
    except ObjectDoesNotExist:
        period = Period(name=period_name)
        period.save()
    return period
