"""clubmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r"^blog/", include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from wiki.urls import get_pattern as get_wiki_patterns
from django_nyt.urls import get_pattern as get_nyt_patterns

from core import urls as api_urls

admin.site.site_header = "Bunker Hills Men's Club Administration"

urlpatterns = [
    url(r"^", include("web.urls")),
    url(r"^admin/", admin.site.urls),
    url(r"^api/", include("core.urls")),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    # this url is used to generate a password reset email
    url(r'^member/reset-password-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),
    url(r'^notifications/', get_nyt_patterns()),
    url(r'^wiki/', get_wiki_patterns()),
    url(r'^login/$', admin.site.login, name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
