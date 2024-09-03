from django.urls import path
from . views import SolutionListView, SolutionCreateView, SolutionDetailView

urlpatterns = [
    path('', SolutionListView.as_view(), name='solutions'),
    path('add/', SolutionCreateView.as_view(), name='add_solution'),
    path('<slug:pk>/', SolutionDetailView.as_view(), name='solution_detail'),
]
