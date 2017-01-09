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
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from core import urls as api_urls

urlpatterns = [
    url(r"^", include("web.urls", namespace="web")),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^api/", include(api_urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    # this url is used to generate a password reset email
    url(r'^member/reset-password-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),
]
