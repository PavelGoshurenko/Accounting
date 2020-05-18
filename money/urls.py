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
]
