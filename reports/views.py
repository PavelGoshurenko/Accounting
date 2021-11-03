from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from goods.models import Sale, Product
from money.models import Spending, Asset, Period, Transfer
from production.models import Ingredient
from django.db.models import Sum, Q
from collections import defaultdict
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import math

# Create your views here.


@login_required
def profit(request):
    sales = Sale.objects.all()
    margin = 0
    for sale in sales:
        margin = margin + sale.price * sale.quantity - sale.purchase_price * sale.quantity
    spendings = Spending.objects.all()
    spendings_amount = 0
    for spending in spendings:
        spendings_amount += spending.amount
    assets = Asset.objects.all()
    assets_amount = 0
    for asset in assets:
        assets_amount += asset.amount
    products = Product.objects.all()
    product_cost = 0
    for product in products:
        product_cost = product_cost + product.quantity * product.purchase_price
    ingredients = Ingredient.objects.all()
    ingredients_cost = 0
    for ingredient in ingredients:
            ingredients_cost += ingredient.quantity * ingredient.purchase_price
    funds = 189390
    electrinics = 146054
    company_cost = assets_amount + product_cost + ingredients_cost + funds + electrinics
    start_company_cost = 987981.69
    periods = Period.objects.all()
    profits_by_periods = []
    check_margin = 0
    check_spendings = 0
    check_profit = 0
    for period in periods:
        sales_by_period = Sale.objects.filter(period=period)
        margin_by_period = 0
        sales_sum_by_period = 0
        for sale in sales_by_period:
            margin_by_period = margin_by_period + sale.price * sale.quantity - sale.purchase_price * sale.quantity
            sales_sum_by_period += sale.price * sale.quantity
        spendings_by_period = Spending.objects.filter(period=period)
        spendings_amount_by_period = 0
        for spending in spendings_by_period:
            spendings_amount_by_period += spending.amount
        pasha_take_by_period = spendings_by_period.aggregate(sum=Sum('amount', filter=Q(name='Pasha take')))
        oleg_take_by_period = spendings_by_period.aggregate(sum=Sum('amount', filter=Q(name='Oleg take')))
        if pasha_take_by_period['sum'] is None:
            pasha_take_by_period['sum'] = 0
        if oleg_take_by_period['sum'] is None:
            oleg_take_by_period['sum'] = 0
        dividents_by_period = pasha_take_by_period['sum'] + oleg_take_by_period['sum']
        profit_by_period = {
            'period': period.name,
            'sales_sum': sales_sum_by_period,
            'margin': round(margin_by_period, 2),
            'spendings_amount': round(spendings_amount_by_period - dividents_by_period, 2),
            'sales_profit': round(margin_by_period - spendings_amount_by_period + dividents_by_period, 2),
            'dividents': dividents_by_period,
        }
        profits_by_periods.append(profit_by_period)
        check_margin += margin_by_period
        check_spendings += spendings_amount_by_period - dividents_by_period
        check_profit += margin_by_period - spendings_amount_by_period + dividents_by_period
    pasha_take = Spending.objects.aggregate(sum=Sum('amount', filter=Q(name='Pasha take')))
    oleg_take = Spending.objects.aggregate(sum=Sum('amount', filter=Q(name='Oleg take')))
    if pasha_take['sum'] is None:
        pasha_take['sum'] = 0
    if oleg_take['sum'] is None:
        pasha_take['sum'] = 0
    dividents = pasha_take['sum'] + oleg_take['sum']
    sales_profit = margin - spendings_amount + dividents
    assets_profit = company_cost - start_company_cost + dividents
    context = {
        'margin': round(margin, 2),
        'spendings_amount': round(spendings_amount - dividents, 2),
        'sales_profit': round(sales_profit, 2),
        'assets_amount': round(assets_amount, 2),
        'product_cost': round(product_cost, 2),
        'ingredient_cost': round(ingredients_cost, 2),
        'company_cost': round(company_cost, 2),
        'funds': round(funds, 2),
        'electronics': round(electrinics, 2),
        'start_company_cost': round(start_company_cost, 2),
        'assets_profit': round(assets_profit, 2),
        'profits_by_periods': profits_by_periods,
        'check_margin': round(check_margin, 2),
        'check_spendings': round(check_spendings, 2),
        'check_profit': round(check_profit, 2),
        'dividents': round(dividents, 2),
    }
    return render(request, 'profit.html', context)

@login_required
def salary(request):
    this_period_name = datetime.datetime.strftime(timezone.now(), '%B %Y')
    try:
        this_period = Period.objects.get(name=this_period_name)
    except ObjectDoesNotExist:
        this_period = Period(name=this_period_name)
        this_period.save()
    last_period_name = datetime.datetime.strftime(timezone.now() + relativedelta(months=-1), '%B %Y')
    last_period = Period.objects.get(name=last_period_name)

    # Anatoliy this period
    Anatoliy_this_period_sales = Sale.objects.filter(manager__username='Anatoliy', period=this_period)
    Anatoliy_this_period_sales_by_dates = defaultdict(int)
    for sale in Anatoliy_this_period_sales:
        Anatoliy_this_period_sales_by_dates[sale.date.strftime("%d.%m.%Y")] += sale.cost()
    Anatoliy_this_period = []
    Anatoliy_this_period_sum = 0
    for date, daily_sales in Anatoliy_this_period_sales_by_dates.items():
        day = {
            'date': date,
            'daily_sales': daily_sales,
            'percent': round(daily_sales * 0.04, 2),
            'rate': 200
        }
        Anatoliy_this_period_sum += 200 + daily_sales * 0.04
        Anatoliy_this_period.append(day)


    # Anatoliy last period
    Anatoliy_last_period_sales = Sale.objects.filter(manager__username='Anatoliy', period=last_period)
    Anatoliy_last_period_sales_by_dates = defaultdict(int)
    for sale in Anatoliy_last_period_sales:
        Anatoliy_last_period_sales_by_dates[sale.date.strftime("%d.%m.%Y")] += sale.cost()
    Anatoliy_last_period = []
    Anatoliy_last_period_sum = 0
    for date, daily_sales in Anatoliy_last_period_sales_by_dates.items():
        day = {
            'date': date,
            'daily_sales': daily_sales,
            'percent': round(daily_sales * 0.04, 2),
            'rate': 200
        }
        Anatoliy_last_period_sum += 200 + daily_sales * 0.04
        Anatoliy_last_period.append(day)

    # Rodion this period
    rodion_this_period_percent = 0.04
    rodion_this_period_rate = 200
    rodion_this_period_sales = Sale.objects.filter(manager__username='Rodion', period=this_period)
    rodion_this_period_sales_by_dates = defaultdict(int)
    for sale in rodion_this_period_sales:
        rodion_this_period_sales_by_dates[sale.date.strftime("%d.%m.%Y")] += sale.cost()
    Rodion_this_period = []
    Rodion_this_period_sum = 0
    for date, daily_sales in rodion_this_period_sales_by_dates.items():
        day = {
            'date': date,
            'daily_sales': daily_sales,
            'percent': round(daily_sales * rodion_this_period_percent, 2),
            'rate': rodion_this_period_rate
        }
        Rodion_this_period_sum += rodion_this_period_rate + daily_sales * rodion_this_period_percent
        Rodion_this_period.append(day)

    # Rodion last period
    rodion_last_period_percent = 0.04
    rodion_last_period_rate = 200
    rodion_last_period_sales = Sale.objects.filter(manager__username='Rodion', period=last_period)
    rodion_last_period_sales_by_dates = defaultdict(int)
    for sale in rodion_last_period_sales:
        rodion_last_period_sales_by_dates[sale.date.strftime("%d.%m.%Y")] += sale.cost()
    Rodion_last_period = []
    Rodion_last_period_sum = 0
    for date, daily_sales in rodion_last_period_sales_by_dates.items():
        day = {
            'date': date,
            'daily_sales': daily_sales,
            'percent': round(daily_sales * rodion_last_period_percent, 2),
            'rate': rodion_last_period_rate,
        }
        Rodion_last_period_sum += rodion_last_period_rate + daily_sales * rodion_last_period_percent
        Rodion_last_period.append(day)
    

    # Bogdan last period
    sales_last_period = Sale.objects.filter(period=last_period)
    margin_last_period = 0
    sales_last_period_sum = 0
    for sale in sales_last_period:
        margin_last_period += sale.price * sale.quantity - sale.purchase_price * sale.quantity
        sales_last_period_sum += sale.cost()
    BOGDAN_RATE = 4000
    Bogdan_percent_last_period = margin_last_period * 0.08
    Bogdan_last_period_sum = BOGDAN_RATE + Bogdan_percent_last_period

    # Bogdan this period
    sales_this_period = Sale.objects.filter(period=this_period)
    margin_this_period = 0
    sales_this_period_sum = 0
    for sale in sales_this_period:
        margin_this_period += sale.price * sale.quantity - sale.purchase_price * sale.quantity
        sales_this_period_sum += sale.cost()
    BOGDAN_RATE = 4000
    Bogdan_percent_this_period = margin_this_period * 0.08
    Bogdan_this_period_sum = BOGDAN_RATE + Bogdan_percent_this_period
    

    context = {
        'this_period': this_period_name,
        'last_period': last_period_name,
        'Rodion_this_period': Rodion_this_period,
        'Rodion_this_period_sum': round(Rodion_this_period_sum, 2),
        'Rodion_last_period': Rodion_last_period,
        'Rodion_last_period_sum': round(Rodion_last_period_sum, 2),
        'Anatoliy_this_period': Anatoliy_this_period,
        'Anatoliy_this_period_sum': round(Anatoliy_this_period_sum, 2),
        'Anatoliy_last_period': Anatoliy_last_period,
        'Anatoliy_last_period_sum': round(Anatoliy_last_period_sum, 2),
        'sales_last_period_sum': sales_last_period_sum,
        'sales_this_period_sum': sales_this_period_sum,
        'margin_last_period': round(margin_last_period, 2),
        'margin_this_period': round(margin_this_period, 2),
        'BOGDAN_RATE': BOGDAN_RATE,
        'Bogdan_percent_last_period': round(Bogdan_percent_last_period, 2),
        'Bogdan_percent_this_period': round(Bogdan_percent_this_period, 2),
        'Bogdan_last_period_sum': round(Bogdan_last_period_sum, 2),
        'Bogdan_this_period_sum': round(Bogdan_this_period_sum, 2),
    }
    return render(request, 'salary.html', context)


@login_required
def oleg(request):
    periods = Period.objects.all()
    profits_by_periods = []
    oleg_debt = 220165
    for period in periods:
        sales_by_period = Sale.objects.filter(period=period)
        margin_by_period = 0
        sales_sum_by_period = 0
        oleg_transfers_sum = 0
        oleg_transfers = []
        for transfer in Transfer.objects.filter(period=period, asset_to__name='Олег'):
            oleg_transfers.append({
                'name': transfer.name,
                'amount': transfer.amount,
            })
            oleg_transfers_sum += transfer.amount
        for transfer in Transfer.objects.filter(period=period, asset_from__name='Олег'):
            oleg_transfers.append({
                'name': transfer.name,
                'amount': -transfer.amount,
            })
            oleg_transfers_sum -= transfer.amount
        for sale in sales_by_period:
            margin_by_period = margin_by_period + sale.price * sale.quantity - sale.purchase_price * sale.quantity
            sales_sum_by_period = sales_sum_by_period + sale.price * sale.quantity
        spendings_by_period = Spending.objects.filter(period=period)
        spendings_amount_by_period = 0
        for spending in spendings_by_period:
            spendings_amount_by_period += spending.amount
        pasha_take_by_period = spendings_by_period.aggregate(sum=Sum('amount', filter=Q(name='Pasha take')))
        oleg_take_by_period = spendings_by_period.aggregate(sum=Sum('amount', filter=Q(name='Oleg take')))
        if pasha_take_by_period['sum'] is None:
            pasha_take_by_period['sum'] = 0
        if oleg_take_by_period['sum'] is None:
            oleg_take_by_period['sum'] = 0
        dividents_by_period = pasha_take_by_period['sum'] + oleg_take_by_period['sum']
        oleg_start_dept = oleg_debt
        diff = {
            'amount': oleg_transfers_sum - oleg_take_by_period['sum'],
            'name': 'Недобор' if (oleg_transfers_sum - oleg_take_by_period['sum']) < 0 else 'Перебор'
        }
        oleg_debt += oleg_transfers_sum - oleg_take_by_period['sum']
        oleg_finish_dept = oleg_debt
        profit_by_period = {
            'period': period.name,
            'sales_sum': sales_sum_by_period,
            'sales_profit': round(margin_by_period - spendings_amount_by_period + dividents_by_period, 2),
            'oleg_dividents': oleg_take_by_period['sum'],
            'oleg_transfers': oleg_transfers,
            'oleg_transfers_sum': oleg_transfers_sum,
            'oleg_start_dept': oleg_start_dept,
            'oleg_finish_dept': oleg_finish_dept,
            'diff': diff,
        }
        profits_by_periods.append(profit_by_period)
    context = {
        'profits_by_periods': profits_by_periods,
    }
    return render(request, 'oleg.html', context)
