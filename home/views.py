from django.shortcuts import render
from solutions.models import Solution
from datetime import datetime


def index(request):
    """ A view to render the home page """
    # query all solutions from the database
    solutions = Solution.objects.all()

    # process the tech_stack for each solution by splitting the string into a list
    for solution in solutions:
        solution.tech_stack = solution.tech_stack.split(", ")
    # Get the current year
    current_year = datetime.now().year

    # passing the processed solution list to a context
    context = {
        'solution_list': solutions,
        'current_year': current_year,
    }

    return render(request, 'home/index.html', context)


# Thank Your Message
def thank_you(request):
    """
    A view to render Thank Your Message
    """

    context = {}

    return render(request, 'home/thank_you.html', context)