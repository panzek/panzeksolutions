from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from solutions.models import Solution
from django.views import generic
from .forms import SolutionForm


@login_required()
def add_solution(request):
    """ A view for store owner to add solution  to the store """

    if not request.user.is_superuser:
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('add_solution'))
    else:
        form = SolutionForm()

    template = 'solutions/add_solution.html'
    context = {
        'form': form
    }

    return render(request, template, context)


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


class SolutionCreateView(generic.edit.CreateView):
    model = Solution
    fields = '__all__'
