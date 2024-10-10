from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from contact.models import Contact
from solutions.models import Solution


class StaticViewSitemap(Sitemap):  # for static pages
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["home", "about"]

    def location(self, item):
        return reverse(item)


class SolutionSitemap(Sitemap):  # sitemap to include all the links to individual solutions entries
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Solution.objects.all()

    def location(self, obj):
        return obj.website_full_url


class ContactSitemap(Sitemap):

    def items(self):
        return Contact.objects.all()

    def location(self, obj):
        return obj.website_full_url
