"""guild_site URL Configuration

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
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .views import IndexPageView, RecruitmentView
from chat import urls as chat_urls
from auth_app import urls as auth_urls


app_patterns = [
    url(r'^chat/', include(chat_urls)),
    url(r'^auth/', include(auth_urls)),
    url(r'^admin/', include(admin.site.urls)),
]


urlpatterns = [
    url(r'^guild_site/$', IndexPageView.as_view(), name='index'),
    url(r'^guild_site/recruitment/$', RecruitmentView.as_view(), name='recruitment'),
    url(r'^guild_site/', include(app_patterns)),
]
