"""
URL configuration for panzek project.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from home.sitemap import SolutionSitemap
from home.sitemap import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'solutions': SolutionSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('contact/', include('contact.urls')),
    path('portfolios/', include('portfolio.urls')),
    path('solutions/', include('solutions.urls')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
