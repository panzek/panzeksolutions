from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('thank_you/', views.thank_you, name='thanks'),
]