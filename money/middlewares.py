from money.models import Period
import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


def expand_context(request):
    period_name = datetime.datetime.strftime(timezone.now(), '%B %Y')
    try:
        period = Period.objects.get(name=period_name)
    except ObjectDoesNotExist:
        period = Period(name=period_name)
        period.save()
    return {'period_id': period.id}
