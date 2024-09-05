from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from solutions.models import Solution
from django.views import generic
from .forms import SolutionForm


# using class-based view
class SolutionListView(generic.ListView):
    model = Solution
    # queryset = Solution.objects.all()
    template_name = 'solution_list.html'
    context_object_name = 'solution_list'
    paginate_by = 4

    # Method to split tech_stack string into a list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for solution in context['solution_list']:
            # Split the tech_stack string into a list
            solution.tech_stack = solution.tech_stack.split(", ")
        return context


# Detail view
class SolutionDetailView(generic.DetailView):
    model = Solution

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tech_stack_list'] = self.object.tech_stack.split(',')
        return context


# create view
class SolutionCreateView(generic.edit.CreateView):
    model = Solution
    fields = '__all__'


# Update view
class SolutionUpdateView(generic.edit.UpdateView):
    model = Solution
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('solutions')


# Delete Solution view
class SolutionDeleteView(generic.edit.DeleteView):
    model = Solution
    success_url = reverse_lazy('solutions')