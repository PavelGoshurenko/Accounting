from django.contrib import admin
from django.urls import path, include
from goods import views
from goods import api

urlpatterns = [
    path('', views.main, name='index'),
    path('all/', views.ProductsView.as_view(), name='products'),
    path('api/add_inv/', api.ProductInvApi.as_view()),
    path('api/', api.ProductApi.as_view(), name='products_api'),
    path('not_active/', views.NotActiveProductsView.as_view(), name='not_active_products'),
    path('order/', views.ProductsOrder.as_view(), name='products_order'),
    path('products/download/', views.download_products, name='download_products'),
    path('products/download_order/', views.download_products_order, name='download_products_order'),
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
    #path('get_internet_products', views.get_internet_products, name='get_internet_products'),
    path('sales_by_products', views.sales_by_products, name='sales_by_products'),
    # invoices
    path('invoices/', views.InvoicesView.as_view(), name='invoices'),
    path('<int:pk>/', views.InvoiceView.as_view(), name='invoice'),
    path('invoice/create/', views.InvoiceCreate.as_view(), name='invoice_create'),
    path('invoice/new/', views.new_invoice, name='new_invoice'),
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
    path('invoice/<int:pk>/download/', views.download_invoice, name='download_invoice'),
    # incomings
    path('incomings/', views.IncomingsView.as_view(), name='incomings'),
    path('incoming/<int:pk>/', views.IncomingView.as_view(), name='incoming'),
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
    path('sales/today/shop', views.TodayShopSalesView.as_view(), name='today_sales_shop'),
    path('sales/today/internet', views.TodayInternetSalesView.as_view(), name='today_sales_internet'),
    path('sale/<int:pk>/', views.SaleView.as_view(), name='sale'),
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
    path('add_sales/shop', views.add_sales_shop, name="add_sales_shop"),
    path('add_sales/internet', views.add_sales_internet, name="add_sales_internet"),
    path('add_sales/internet2', views.add_sales_internet2, name="add_sales_internet2"),
    path('add_sales/shop2', views.add_sales_shop2, name="add_sales_shop2"),
    # inventory
    path('add_inventories', views.add_inventories, name="add_inventories"),
    path('add_inventories2', views.add_inventories2, name="add_inventories2"),
    path('inventories', views.inventories, name='inventories'),
    path('confirm_inventories', views.confirm_inventories, name='confirm_inventories'),
    path('inventories_result/', views.InventoriesResult.as_view(), name='inventories_result'),
    # tasks
    path('task/create/', views.TaskCreate.as_view(), name='task_create'),
    path('tasks', views.TasksView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TaskView.as_view(), name='task'),
    path('tasks/create_from_invoice/<int:pk>/', views.task_from_invoice, name='task_from_invoice'),
    path('tasks/confirm/<int:pk>/', views.confirm_task, name='confirm_task'),
]
