from django.urls import path
from . views import SolutionListView, SolutionCreateView

urlpatterns = [
    path('', SolutionListView.as_view(), name='solutions'),
    path('add/', SolutionCreateView.as_view(), name='add_solution'),
]
