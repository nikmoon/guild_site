from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout

from guild_site.settings import GUILD, PROJECT_URL
from .forms import LoginForm 

import json
from tornado.httpclient import HTTPClient, HTTPRequest
from guild_site.settings import COMET_SERVER, COMET_URL_NOTIFY_USER_LOGIN, COMET_URL_NOTIFY_USER_LOGOUT

# Create your views here.


# Пользователи, вошедшие на сайт
Users = {}


def send_comet_notification(data, notifyURL):
    url = COMET_SERVER + notifyURL
    request = HTTPRequest(url, method='POST', body=json.dumps(data))
    try:
        HTTPClient().fetch(request)
    except Exception:
        pass


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    nextPage = request.GET.get('next', PROJECT_URL)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                Users[request.session.session_key] = user
                send_comet_notification(
                    {'username': username, 'sessionid': request.session.session_key},
                    COMET_URL_NOTIFY_USER_LOGIN
                )
                return HttpResponseRedirect(nextPage)
    else:
        form = LoginForm()

    return render(request, 'auth_app/login.html', {'guild': GUILD, 'form': form, 'next': nextPage})


def logout_view(request):
    sessionid = request.session.session_key
    logout(request)
    if sessionid in Users:
        del Users[sessionid]
    send_comet_notification(
        {'username': request.user.username, 'sessionid': sessionid},
        COMET_URL_NOTIFY_USER_LOGOUT
    )
    return HttpResponseRedirect(reverse('index'))

