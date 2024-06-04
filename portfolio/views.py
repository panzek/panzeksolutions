from django.shortcuts import render

# Create your views here.

def portfolio(request):
    """ A view to render the portfolio page """

    template = 'portfolios/portfolio.html'

    return render(request, template)
