# coding:utf-8
"""WebDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'pcapdisplay.views.home'),
    url(r'^distribution/', 'pcapdisplay.views.host_distribution_page'),
    url(r'^api/time/$','pcapdisplay.views.time_distribution_json'),
    url(r'^api/geography/$','pcapdisplay.views.geography_distribution_json'),
    url(r'^api/content/$','pcapdisplay.views.content_distribution_json'),
    url(r'^api/host/$','pcapdisplay.views.host_distribution_page'),
]
