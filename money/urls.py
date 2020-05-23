from django.contrib import admin
from django.urls import path, include
from money import views

urlpatterns = [
    path('', views.SpendingsView.as_view(), name='spendings'),
    path('<int:pk>/', views.SpendingView.as_view(), name='spending'),
    path('spending/create/', views.SpendingCreate.as_view(), name='spending_create'),
    path(
        'spending/<int:pk>/update/',
        views.SpendingUpdate.as_view(),
        name='spending_update'
        ),
    path(
        'spending/<int:pk>/delete/',
        views.SpendingDelete.as_view(),
        name='spending_delete'
        ),
    # assets
    path('assets/', views.AssetsView.as_view(), name='assets'),
    path('<int:pk>/', views.AssetView.as_view(), name='asset'),
    path('asset/create/', views.AssetCreate.as_view(), name='asset_create'),
    path(
        'asset/<int:pk>/update/',
        views.AssetUpdate.as_view(),
        name='asset_update'
        ),
    path(
        'asset/<int:pk>/delete/',
        views.AssetDelete.as_view(),
        name='asset_delete'
        ),
]
