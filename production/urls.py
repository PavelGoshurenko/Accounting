from django.contrib import admin
from django.urls import path, include
from production import views

urlpatterns = [
    path('', views. IngredientsView.as_view(), name='ingredients'),
    path('<int:pk>/', views.IngredientView.as_view(), name='ingredient'),
    path('ingredient/create/', views.IngredientCreate.as_view(), name='ingredient_create'),
    path(
        'ingredient/<int:pk>/update/',
        views.IngredientUpdate.as_view(),
        name='ingredient_update'
        ),
    path(
        'ingredient/<int:pk>/delete/',
        views.IngredientDelete.as_view(),
        name='ingredient_delete'
        ),
    path('add_ingredient_from_file/', views.AddIngredientsView.as_view(), name='add_ingredients_from_file'),
    path('ingredient_invoices/', views.IngredientInvoicesView.as_view(), name='ingredient_invoices'),
    path('<int:pk>/', views.IngredientInvoiceView.as_view(), name='ingredient_invoice'),
    path('ingredient_invoice/create/', views.IngredientInvoiceCreate.as_view(), name='ingredient_invoice_create'),
    path('ingredient_invoice/new/', views.new_ingredient_invoice, name='new_ingredient_invoice'),
    path(
        'ingredient_invoice/<int:pk>/update/',
        views.IngredientInvoiceUpdate.as_view(),
        name='ingredient_invoice_update'
        ),
    path(
        'ingredient_invoice/<int:pk>/delete/',
        views.IngredientInvoiceDelete.as_view(),
        name='ingredient_invoice_delete'
        ),
    path('ingredient_incomings/', views.IngredientIncomingsView.as_view(), name='ingredient_incomings'),
    path('<int:pk>/', views.IngredientIncomingView.as_view(), name='ingredient_incoming'),
    path('ingredient_incoming/create/', views.IngredientIncomingCreate.as_view(), name='ingredient_incoming_create'),
    path(
        'ingredient_incoming/<int:pk>/update/',
        views.IngredientIncomingUpdate.as_view(),
        name='ingredient_incoming_update'
        ),
    path(
        'ingredient_incoming/<int:pk>/delete/',
        views.IngredientIncomingDelete.as_view(),
        name='ingredient_incoming_delete'
        ),
    # manufacturings
    path('manufacturings/', views.ManufacturingsView.as_view(), name='manufacturings'),
    path('<int:pk>/', views.ManufacturingView.as_view(), name='manufacturing'),
    path('manufacturing/create/', views.ManufacturingCreate.as_view(), name='manufacturing_create'),
    path(
        'manufacturing/<int:pk>/update/',
        views.ManufacturingUpdate.as_view(),
        name='manufacturing_update'
        ),
    path(
        'manufacturing/<int:pk>/delete/',
        views.ManufacturingDelete.as_view(),
        name='manufacturing_delete'
        ),
]