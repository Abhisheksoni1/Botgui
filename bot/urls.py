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
from bot import views
from django.contrib.auth.views import logout



urlpatterns = [
    url(r'^sign-out/$', logout, {'template_name': 'index.html', 'next_page': '/'}, name='sign-out'),
    url(r'^$', views.index, name='index'),
    url(r'^services', views.services, name='services'),
    url(r'^index', views.index, name='index'),
    url(r'^index-2', views.index2, name='index-2'),
    url(r'^index-3', views.index3, name='index-3'),
    url(r'^about', views.about, name='about'),
    url(r'^404', views.error, name='404'),
    url(r'^blog-details', views.blog_details, name='blog-details'),
    url(r'^blog-list', views.blog_list, name='blog-list'),
    url(r'^cart', views.cart, name='cart'),
    url(r'^comming-soon', views.comming_soon, name='comming-soon'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^login-signup', views.login_signup, name='login-signup'),
    url(r'^product-details', views.product_details, name='product-details'),
    url(r'^product-grid', views.product_grid, name='product-grid'),
    url(r'^product-list', views.product_list, name='product-list'),
    url(r'^support', views.support, name='support'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^login', views.login_view, name='login'),
    url(r'^email_subscribe', views.email_subscribe, name='email_subscribe'),
    # url(r'^time$', views.time, name='time'),
    # url('^symbols', views.symbols, name='symbols'),
    # url('^search', views.search, name='search'),
    # url('^history', views.history, name='history'),
]
