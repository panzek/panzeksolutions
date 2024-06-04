from django.shortcuts import render

# Create your views here.

def portfolios(request):
    """ A view to render the portfolio page """

    template = 'portfolio/portfolios.html'

    return render(request, template)
