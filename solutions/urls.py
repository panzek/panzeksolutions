from django.urls import path
from . views import SolutionListView, SolutionCreateView, SolutionDetailView, SolutionUpdateView, SolutionDeleteView

urlpatterns = [
    path('', SolutionListView.as_view(), name='solutions'),
    path('add/', SolutionCreateView.as_view(), name='add_solution'),
    path('<int:pk>/', SolutionDetailView.as_view(), name='solution_detail'),
    path('<int:pk>/edit', SolutionUpdateView.as_view(), name='solution_edit'),
    path('<int:pk>/delete', SolutionDeleteView.as_view(), name='solution_delete'),
]
