from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from goods.models import Sale, Product
from money.models import Spending, Asset, Period
from production.models import Ingredient

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
    sales_profit = margin - spendings_amount
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
    assets_profit = company_cost - start_company_cost
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
        profit_by_period = {
            'period': period.name,
            'margin': margin_by_period,
            'spendings_amount': spendings_amount_by_period,
            'sales_profit': margin_by_period - spendings_amount_by_period,
        }
        profits_by_periods.append(profit_by_period)
        check_margin += margin_by_period
        check_spendings += spendings_amount_by_period
        check_profit += margin_by_period - spendings_amount_by_period
    context = {
        'margin': margin,
        'spendings_amount': spendings_amount,
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
    }
    return render(request, 'profit.html', context)


