from django.urls import path
from . views import SolutionListView

urlpatterns = [
    path('', SolutionListView.as_view(), name='solutions'),
]
