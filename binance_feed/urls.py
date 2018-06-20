"""tiago_btf_exchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from binance_feed import views

urlpatterns = [
    url(r'^config$', views.config, name='config'),
    url(r'^time$', views.time, name='time'),
    url(r'^symbols', views.symbols, name='symbols'),
    url(r'^search', views.search, name='search'),
    url(r'^history', views.history, name='history'),
    url(r'^ticker/(?P<symbol>\w+)/$', views.ticker, name='ticker'),
]
