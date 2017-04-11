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
#from django.contrib import admin
#from .views import IndexPageView, RecruitmentView
#from chat import urls as chat_urls

from . import views


urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
#    url(r'^userinfo/$', views.UserInfoView.as_view(), name='user_info'),
#    url(r'^users/$', views.UsersView.as_view(), name='users'),

    
    #url(r'^$', IndexPageView.as_view(), name='index'),
    #url(r'recruitment', RecruitmentView.as_view(), name='recruitment'),
    #url(r'chat/', include(chat_urls)),
    #url(r'admin/', include(admin.site.urls)),
]

