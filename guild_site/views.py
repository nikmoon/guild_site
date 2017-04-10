from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView, View
from .models import NewsItem

#from .settings import GUILD
from . import settings


class MySecretView(View):

    def dispatch(self, request, *args, **kwargs):
        secret = request.GET.get('secret')
        if True:
        #if secret and secret == settings.SECRET_KEY:
            return super(MySecretView, self).dispatch(request, *args, **kwargs)

        return HttpResponse('Вам сюда нельзя', status=401)



class IndexPageView(TemplateView):

    template_name = 'guild_site/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['guild'] = settings.GUILD
        context['news'] = NewsItem.objects.order_by('-id')[:5]
        return context


class RecruitmentView(TemplateView):

    template_name = 'guild_site/recruitment.html'

    def get_context_data(self, **kwargs):
        context = super(RecruitmentView, self).get_context_data(**kwargs)
        context['guild'] = settings.GUILD
        return context


'''
from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=80)
    file = forms.FileField()


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            with open('db.sqlite3.from_client', "wb+") as dest_file:
                for chunk in request.FILES['file'].chunks():
                    dest_file.write(chunk)
            return HttpResponseRedirect('/django/')
    else:
        form = UploadFileForm()
    return render(request, 'guild_site/upload.html', {'guild': GUILD, 'form': form} )
'''

