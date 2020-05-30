from django.contrib import admin
from django.urls import path, include
from goods import views

urlpatterns = [
    path('', views.ProductsView.as_view(), name='products'),
    path('<int:pk>/', views.ProductView.as_view(), name='product'),
    path('product/create/', views.ProductCreate.as_view(), name='product_create'),
    path(
        'product/<int:pk>/update/',
        views.ProductUpdate.as_view(),
        name='product_update'
        ),
    path(
        'product/<int:pk>/delete/',
        views.ProductDelete.as_view(),
        name='product_delete'
        ),
    path('add_products_from_file/', views.AddProductsView.as_view(), name='add_products_from_file'),
    path('add_incomings/', views.add_incomings, name="add_incomings"),
    path('invoices/', views.InvoicesView.as_view(), name='invoices'),
    path('<int:pk>/', views.InvoiceView.as_view(), name='invoice'),
    path('invoice/create/', views.InvoiceCreate.as_view(), name='invoice_create'),
    path(
        'invoice/<int:pk>/update/',
        views.InvoiceUpdate.as_view(),
        name='invoice_update'
        ),
    path(
        'invoice/<int:pk>/delete/',
        views.InvoiceDelete.as_view(),
        name='invoice_delete'
        ),
    path('incomings/', views.IncomingsView.as_view(), name='incomings'),
    path('<int:pk>/', views.IncomingView.as_view(), name='incoming'),
    path('incoming/create/', views.IncomingCreate.as_view(), name='incoming_create'),
    path(
        'incoming/<int:pk>/update/',
        views.IncomingUpdate.as_view(),
        name='incoming_update'
        ),
    path(
        'incoming/<int:pk>/delete/',
        views.IncomingDelete.as_view(),
        name='incoming_delete'
        ),
    # sales
    path('sales/', views.SalesView.as_view(), name='sales'),
    path('<int:pk>/', views.SaleView.as_view(), name='sale'),
    path('sale/create/', views.SaleCreate.as_view(), name='sale_create'),
    path(
        'sale/<int:pk>/update/',
        views.SaleUpdate.as_view(),
        name='sale_update'
        ),
    path(
        'sale/<int:pk>/delete/',
        views.SaleDelete.as_view(),
        name='sale_delete'
        ),
]
