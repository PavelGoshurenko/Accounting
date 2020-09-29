
from money.models import Asset
from django.core.exceptions import ObjectDoesNotExist
import datetime


def get_asset(department):
    asset_name = '{} {}'.format(datetime.date.today(), department)
    try:
        asset = Asset.objects.get(name=asset_name)
    except ObjectDoesNotExist:
        asset = Asset(name=asset_name, amount=0)
        asset.save()
    return asset
