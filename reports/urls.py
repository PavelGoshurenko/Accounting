from django.contrib import admin
from django.urls import path, include
from reports import views

urlpatterns = [
    path('profit', views.profit, name="profit"),
]
