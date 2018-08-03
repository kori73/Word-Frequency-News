"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from news.views import word_count_list, bar_graph, ChartData


urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('home/', word_count_list, name='home'),
    path('homebar/', bar_graph, name="bar_graph_url"),
    re_path(r'^api/chart/data/$', ChartData.as_view(), name="api_chart_data"),

]