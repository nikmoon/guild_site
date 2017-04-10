
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout

import json
from tornado.httpclient import HTTPClient, HTTPRequest

from .forms import LoginForm 
from guild_site import settings

# Create your views here.


# Пользователи, вошедшие на сайт
Users = {}


def send_comet_notification(data, notifyURL):
    url = settings.COMET_SERVER + notifyURL
    request = HTTPRequest(url, method='POST', body=json.dumps(data))
    try:
        HTTPClient().fetch(request)
    except Exception:
        pass


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    nextPage = request.GET.get('next', settings.PROJECT_URL)

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
                    settings.COMET_URL_NOTIFY_LOGIN
                )
                return HttpResponseRedirect(nextPage)
    else:
        form = LoginForm()

    return render(request, 'auth_app/login.html', {'guild': settings.GUILD, 'form': form, 'next': nextPage})


def logout_view(request):
    sessionid = request.session.session_key
    logout(request)
    if sessionid in Users:
        del Users[sessionid]
    send_comet_notification(
        {'username': request.user.username, 'sessionid': sessionid},
        settings.COMET_URL_NOTIFY_LOGOUT
    )
    return HttpResponseRedirect(reverse('index'))


def users_view(request):
    if request.body:
        data = json.loads(request.body.decode('utf-8'))
        if 'secret' in data and data['secret'] == settings.SECRET_KEY:
            return HttpResponse(json.dumps({ sessionID: Users[sessionID].username for sessionID in Users}))

    return HttpResponse('вам сюда нельзя', status=401)


