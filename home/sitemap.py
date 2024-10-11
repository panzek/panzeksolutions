from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from solutions.models import Solution


class StaticViewSitemap(Sitemap):  # for static pages ("home", "contact", "about", etc)
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["home", 'contact']

    def location(self, item):
        return reverse(item)


class SolutionSitemap(Sitemap):  # sitemap to include all the links to individual solutions entries
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Solution.objects.all()

    def location(self, item):
        return reverse('solution_detail', kwargs={'pk': item.pk})

