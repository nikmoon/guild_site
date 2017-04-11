
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView, View

from .models import NewsItem

from . import settings


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


