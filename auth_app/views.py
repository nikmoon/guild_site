
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View


from .forms import LoginForm 
from guild_site import settings

# Create your views here.


class LoginView(View):

    def dispatch(self, request, *args, **kwargs):
        self.nextPage = request.GET.get('next', settings.PROJECT_URL)

        if request.user.is_authenticated():
            return HttpResponseRedirect(self.nextPage)

        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        form = LoginForm()
        return render(request, 'auth_app/login.html', {'guild': settings.GUILD, 'form': form, 'next': self.nextPage})

    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(self.nextPage)
        return render(request, 'auth_app/login.html', {'guild': settings.GUILD, 'form': form, 'next': self.nextPage})



class LogoutView(View):

    def get(self, request):
        sessionid = request.session.session_key
        nextPage = request.GET.get('next', settings.PROJECT_URL)
        logout(request)
        return HttpResponseRedirect(nextPage)


