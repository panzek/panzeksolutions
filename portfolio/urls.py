from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolios, name='portfolios'),
]