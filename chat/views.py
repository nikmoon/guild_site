
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

import json
import requests

from .models import ChatMessage
from guild_site import settings




class IndexView(TemplateView):

    template_name = 'chat/chat.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guild'] = settings.GUILD
        context['urlGetMsg'] = settings.COMET_MSG_URL
        context['urlPostMsg'] = reverse('messages')
        context['lastID'] = ChatMessage.objects.order_by('-id')[0].id
        return context



class MessagesView(View):
    #
    #   POST - запись в БД нового сообщения
    #   GET - получение сообщений из БД
    #

    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({'error': 'Unknown user'}, status=403)

        newMessage = ChatMessage.objects.create(msgText=request.body, msgAuthor=request.user)
        requests.post(settings.COMET_SERVER + settings.COMET_MSG_URL, data=json.dumps({
            'username': request.user.username,
            'messages': [newMessage.to_dict()],
            'secret': settings.SECRET_KEY,
        }))
        return JsonResponse({})


    def get(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({'error': 'Unknown user'}, status=403)

        data = {'username': request.user.username}

        lastID = request.GET.get('lastid')
        if lastID:
            try:
                lastID = int(lastID)
                data['messages'] = [msg.to_dict() for msg in ChatMessage.objects.filter(id__gt=lastID).order_by('id')]
            except ValueError:
                return JsonResponse({'error': 'Invalid lastid'}, status=400)
            except Exception:
                return JsonResponse({'error': 'Unknown error on JsonResponse with lastid parameter'}, status=400)
        else:
            data['messages'] = [msg.to_dict() for msg in ChatMessage.objects.order_by('-id')[:20]][::-1]
        return JsonResponse(data)


    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


