from django.shortcuts import render
from solutions.models import Solution
from django.views import generic


# using class-based view
class SolutionListView(generic.ListView):
    model = Solution
    queryset = Solution.objects.all()
    template_name = 'solution_list.html'
    paginate_by = 4

