from money.models import Period
from goods.models import Task
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
    if request.user.is_authenticated:
        user = request.user
        if user.username == 'fisher':
            tasks = Task.objects.filter(done=False)
        else:
            tasks = Task.objects.filter(user_to=user, done=False)
        tasks_count = tasks.count()
    else:
        tasks_count = 0
    return {'period_id': period.id, 'tasks_count': tasks_count}
