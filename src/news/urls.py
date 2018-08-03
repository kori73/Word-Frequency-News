from django.contrib import admin
from django.urls import path, re_path, include

from .views import scrape

app_name = 'news'

urlpatterns = [
    re_path(r'^scrape/$', scrape, name='scrape_url'),
]
