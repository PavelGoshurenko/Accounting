from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from goods.models import Sale, Product
from money.models import Spending, Asset, Period
from production.models import Ingredient
from django.db.models import Sum, Q

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
        for sale in sales_by_period:
            margin_by_period = margin_by_period + sale.price * sale.quantity - sale.purchase_price * sale.quantity
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
            'margin': margin_by_period,
            'spendings_amount': spendings_amount_by_period - dividents_by_period,
            'sales_profit': margin_by_period - spendings_amount_by_period + dividents_by_period,
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
        'margin': margin,
        'spendings_amount': spendings_amount - dividents,
        'sales_profit': sales_profit,
        'assets_amount': assets_amount,
        'product_cost': product_cost,
        'ingredient_cost': ingredients_cost,
        'company_cost': company_cost,
        'funds': funds,
        'electronics': electrinics,
        'start_company_cost': start_company_cost,
        'assets_profit': assets_profit,
        'profits_by_periods': profits_by_periods,
        'check_margin': check_margin,
        'check_spendings': check_spendings,
        'check_profit': check_profit,
        'dividents': dividents,
    }
    return render(request, 'profit.html', context)
