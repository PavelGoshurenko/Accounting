from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from goods.models import Sale, Product
from money.models import Spending, Asset
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
    }
    return render(request, 'profit.html', context)
